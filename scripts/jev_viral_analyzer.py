#!/usr/bin/env python3
"""Score X posts for viral potential with the TypeSafe System One Jev API."""

import argparse
import datetime
import json
import os
import pathlib
import random
import re
import statistics
import sys
import time
import urllib.request


API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
MAX_ATTEMPTS = 5
TIMEOUT_SECONDS = 30


class FatalError(Exception):
    pass


class SkipPostError(Exception):
    def __init__(self, message, attempts=1):
        super().__init__(message)
        self.attempts = attempts


def repo_root():
    return pathlib.Path(__file__).resolve().parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Score X posts for viral potential via TypeSafe System One Jev."
    )
    parser.add_argument("--input", required=True, help="JSONL corpus path.")
    parser.add_argument(
        "--out",
        default="data/jev_viral_analysis",
        help="Output directory, relative to repo root unless absolute.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means all posts.")
    parser.add_argument(
        "--tag",
        default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        help="Output tag. Default: UTC date YYYY-MM-DD.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print first request with masked Authorization, then exit.",
    )
    return parser.parse_args()


def read_api_key():
    env_key = os.environ.get("TYPESAFE_API_KEY")
    if env_key:
        return env_key

    config_path = pathlib.Path.home() / ".hermes" / "config.yaml"
    if not config_path.exists():
        raise FatalError(
            "Missing TYPESAFE_API_KEY: set the environment variable or configure ~/.hermes/config.yaml."
        )

    in_env = False
    key_pattern = re.compile(
        r'^\s{2}TYPESAFE_API_KEY\s*:\s*(?:"([^"]*)"|\'([^\']*)\'|([^#\s]+))\s*(?:#.*)?$'
    )
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if re.match(r"^env\s*:\s*(?:#.*)?$", line):
                    in_env = True
                    continue
                stripped = line.strip()
                if in_env and stripped and not line.startswith((" ", "\t")):
                    in_env = False
                if not in_env:
                    continue
                match = key_pattern.match(line.rstrip("\n"))
                if match:
                    key = next(value for value in match.groups() if value is not None)
                    if key:
                        return key
    except OSError as exc:
        raise FatalError(f"Could not read config file: {exc}") from exc

    raise FatalError(
        "Missing TYPESAFE_API_KEY: set the environment variable or configure ~/.hermes/config.yaml."
    )


def resolve_path(value, base):
    path = pathlib.Path(value)
    if path.is_absolute():
        return path
    return base / path


def parse_created_at(value):
    if not value or not isinstance(value, str):
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        created = datetime.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if created.tzinfo is None:
        created = created.replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    age = (now - created.astimezone(datetime.timezone.utc)).total_seconds() / 3600.0
    return round(age, 2)


def compact_state(post):
    raw_text = post.get("text", "")
    text = "" if raw_text is None else str(raw_text)[:1200]
    post_state = {"text": text}
    author = post.get("author")
    if isinstance(author, str) and author:
        post_state["author"] = author
    metrics = post.get("metrics")
    if isinstance(metrics, dict):
        post_state["metrics"] = metrics
    age_hours = parse_created_at(post.get("created_at"))
    if age_hours is not None:
        post_state["age_hours"] = age_hours
    return {"post": post_state}


def questions():
    return {
        "hook_strength": {
            "type": "score",
            "instructions": (
                "Rate the scroll-stopping power of the FIRST LINE of `post.text` "
                "for a technically skilled AI-agent-builder audience."
            ),
            "criteria": [
                "scrolls past instantly",
                "weak — generic opener",
                "decent — mild curiosity",
                "strong — specific claim, number or scene in line 1",
                "must-stop — contrarian or concrete result in line 1",
            ],
        },
        "dwell_potential": {
            "type": "score",
            "instructions": (
                "How much of `post.text` rewards staying and processing "
                "(dense numbers, mini-story, list, technical detail)?"
            ),
            "criteria": [
                "nothing to process",
                "light",
                "moderate",
                "dense",
                "very dense, invites re-read",
            ],
        },
        "reply_potential": {
            "type": "score",
            "instructions": (
                "How likely does `post.text` provoke practitioner replies "
                "(open question, contested claim, asks for others' experience)?"
            ),
            "criteria": ["none", "unlikely", "possible", "likely", "very likely"],
        },
        "profile_click_potential": {
            "type": "score",
            "instructions": (
                "Does `post.text` signal lived credibility that makes a reader "
                "check who wrote it?"
            ),
            "criteria": ["none", "weak", "some", "strong", "very strong"],
        },
        "follow_potential": {
            "type": "score",
            "instructions": (
                "Would `post.text` convert a niche reader into a follower of the author?"
            ),
            "criteria": ["no", "weak", "moderate", "strong", "very strong"],
        },
        "has_url_in_body": {
            "type": "noul",
            "instructions": "Does `post.text` contain a URL in the body?",
        },
        "is_engagement_bait": {
            "type": "noul",
            "instructions": "Does `post.text` use engagement bait?",
            "criteria": {
                "true": "Asks for likes/reposts/comments or 'comment X' style bait",
                "false": "No engagement bait",
            },
        },
        "is_allcaps_shout": {
            "type": "noul",
            "instructions": "Is the hook line written in ALL-CAPS shouting style?",
            "criteria": {
                "true": "Hook line is written in ALL-CAPS shouting style",
                "false": "Normal casing",
            },
        },
        "is_offtopic_niche": {
            "type": "noul",
            "instructions": (
                "Is `post.text` outside the AI-agent-builder niche?"
            ),
            "criteria": {
                "true": (
                    "NOT about AI agents, coding agents, agent infrastructure, "
                    "LLM tooling or building AI products"
                ),
                "false": "On-topic for the niche",
            },
        },
        "format_class": {
            "type": "choice",
            "instructions": "Classify the format of `post.text`.",
            "criteria": {
                "war_story": "first-person lived experience with concrete events",
                "tutorial_howto": "teaches a procedure step by step",
                "hot_take": "opinionated claim, little evidence",
                "announcement_news": "news, release or launch report",
                "question_thread": "asks the audience a question to start discussion",
                "list_roundup": "curated list of items/resources",
                "quote_reaction": "reaction to someone else's post",
                "other": "none of the above",
            },
        },
    }


def build_payload(post):
    return {"state": compact_state(post), "model": MODEL, "questions": questions()}


def load_existing_ids(results_path):
    ids = set()
    if not results_path.exists():
        return ids
    with results_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(item, dict):
                continue
            if item.get("success") is False:
                continue
            post_id = item.get("id")
            if post_id is not None:
                ids.add(str(post_id))
    return ids


def load_resume_state(results_path, errors_path):
    results = []
    failures = 0
    result_rows = 0

    if results_path.exists():
        with results_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(item, dict):
                    continue
                result_rows += 1
                if item.get("success") is False:
                    failures += 1
                    continue
                results.append(item)

    error_rows = 0
    if errors_path.exists():
        with errors_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    error_rows += 1

    failures += error_rows
    request_count = result_rows + error_rows
    return results, failures, request_count


def read_posts(input_path, limit):
    if not input_path.exists():
        raise FatalError(f"Input file does not exist: {input_path}")

    posts = []
    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if limit and len(posts) >= limit:
                break
            if not line.strip():
                continue
            try:
                post = json.loads(line)
            except json.JSONDecodeError as exc:
                if line_number == 1:
                    raise FatalError(f"Malformed first line in input JSONL: {exc}") from exc
                post = {
                    "id": f"line-{line_number}",
                    "_read_error": f"Malformed JSON on line {line_number}: {exc}",
                }
            if not isinstance(post, dict):
                if line_number == 1:
                    raise FatalError("Malformed first line in input JSONL: expected object.")
                post = {
                    "id": f"line-{line_number}",
                    "_read_error": f"Expected JSON object on line {line_number}.",
                }
            posts.append(post)
    return posts


def http_post(payload, api_key):
    body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    retry_once_done = False
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body), attempt
        except Exception as exc:
            code = getattr(exc, "code", None)
            if code == 401:
                raise FatalError("TypeSafe API authentication failed with HTTP 401.") from exc
            if code == 422:
                raise SkipPostError(
                    "TypeSafe API rejected the post with HTTP 422.", attempt
                ) from exc
            if code in (429, 529):
                if attempt >= MAX_ATTEMPTS:
                    raise SkipPostError(
                        f"TypeSafe API returned HTTP {code} after {attempt} attempts.",
                        attempt,
                    ) from exc
                delay = (2 ** attempt) + random.random()
                time.sleep(delay)
                continue
            if code and 500 <= code <= 599:
                if retry_once_done:
                    raise SkipPostError(
                        f"TypeSafe API returned HTTP {code} after retry.", attempt
                    ) from exc
                retry_once_done = True
                time.sleep(2 + random.random())
                continue
            raise SkipPostError(f"Request failed: {exc}", attempt) from exc


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_answer(response, post_id):
    answers = response.get("answers", {})
    usage = response.get("usage", {})
    score_keys = [
        "hook_strength",
        "dwell_potential",
        "reply_potential",
        "profile_click_potential",
        "follow_potential",
    ]
    noul_keys = [
        "has_url_in_body",
        "is_engagement_bait",
        "is_allcaps_shout",
        "is_offtopic_niche",
    ]

    if not isinstance(answers, dict):
        raise SkipPostError("TypeSafe response missing answers object.", 0)

    scores = {}
    confidence = {}
    for key in score_keys:
        answer = answers.get(key, {})
        if not isinstance(answer, dict) or "score" not in answer:
            raise SkipPostError(f"TypeSafe response missing score answer: {key}.", 0)
        scores[key] = number(answer.get("score"))
        if "confidence" in answer:
            confidence[key] = number(answer.get("confidence"))

    composite_0_4 = (
        0.30 * scores["hook_strength"]
        + 0.20 * scores["dwell_potential"]
        + 0.20 * scores["reply_potential"]
        + 0.15 * scores["profile_click_potential"]
        + 0.15 * scores["follow_potential"]
    )
    scores["composite_0_4"] = round(composite_0_4, 4)
    scores["composite_0_10"] = round(composite_0_4 * 2.5, 2)

    nouls = {}
    for key in noul_keys:
        answer = answers.get(key, {})
        if not isinstance(answer, dict) or "noul" not in answer:
            raise SkipPostError(f"TypeSafe response missing noul answer: {key}.", 0)
        nouls[key] = number(answer.get("noul"))
        if "confidence" in answer:
            confidence[key] = number(answer.get("confidence"))

    format_answer = answers.get("format_class", {})
    if not isinstance(format_answer, dict) or "choice" not in format_answer:
        raise SkipPostError("TypeSafe response missing choice answer: format_class.", 0)
    format_class = str(format_answer.get("choice", "other"))
    format_confidence = number(format_answer.get("confidence"))
    if "confidence" in format_answer:
        confidence["format_class"] = format_confidence

    return {
        "id": str(post_id),
        "scores": scores,
        "nouls": nouls,
        "format_class": format_class,
        "format_confidence": format_confidence,
        "confidence": confidence,
        "usage": {
            "input_tokens": int(number(usage.get("input_tokens"), 0)),
            "output_tokens": int(number(usage.get("output_tokens"), 0)),
        },
    }


def append_jsonl(path, item):
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=True, sort_keys=True) + "\n")


def first_text(post, limit=100):
    text = str(post.get("text", "")).replace("\n", " ").strip()
    return text[:limit]


def summarize_metrics(post):
    metrics = post.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        return ""
    compact = {key: metrics[key] for key in sorted(metrics)}
    return json.dumps(compact, ensure_ascii=True, sort_keys=True)


def percent(part, whole):
    if whole <= 0:
        return 0.0
    return round((part / whole) * 100.0, 2)


def write_report(path, results, failures, wall_time, request_count, posts_by_id):
    total_input = sum(item["usage"].get("input_tokens", 0) for item in results)
    total_output = sum(item["usage"].get("output_tokens", 0) for item in results)
    score_keys = [
        "hook_strength",
        "dwell_potential",
        "reply_potential",
        "profile_click_potential",
        "follow_potential",
    ]
    anti_keys = [
        "has_url_in_body",
        "is_engagement_bait",
        "is_allcaps_shout",
        "is_offtopic_niche",
    ]

    formats = {}
    for item in results:
        formats[item["format_class"]] = formats.get(item["format_class"], 0) + 1

    lines = [
        f"# Jev Viral Analysis Report {path.stem.removeprefix('report_')}",
        "",
        f"- post count: {len(results)}",
        f"- failures: {failures}",
        f"- this-run wall time seconds: {round(wall_time, 2)}",
        f"- total input tokens: {total_input}",
        f"- total output tokens: {total_output}",
        f"- request count: {request_count}",
        "",
        "## TOP-15 by composite",
        "",
        "| id | format_class | composite_0_10 | first 100 chars | metrics |",
        "| --- | --- | ---: | --- | --- |",
    ]

    top = sorted(
        results, key=lambda item: item["scores"].get("composite_0_10", 0), reverse=True
    )[:15]
    for item in top:
        post = posts_by_id.get(str(item["id"]), {})
        text = first_text(post).replace("|", "\\|")
        metrics = summarize_metrics(post).replace("|", "\\|")
        lines.append(
            f"| {item['id']} | {item['format_class']} | "
            f"{item['scores'].get('composite_0_10', 0)} | {text} | {metrics} |"
        )

    lines.extend(["", "## Format Class Distribution", ""])
    if formats:
        for name, count in sorted(formats.items()):
            lines.append(f"- {name}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Anti-Pattern Shares", ""])
    for key in anti_keys:
        flagged = sum(1 for item in results if item["nouls"].get(key, 0) >= 0.5)
        lines.append(f"- {key}: {percent(flagged, len(results))}%")

    lines.extend(["", "## Per-Score-Question Means", ""])
    for key in score_keys:
        values = [item["scores"].get(key, 0) for item in results]
        mean_value = round(statistics.mean(values), 3) if values else 0.0
        lines.append(f"- {key}: {mean_value}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dry_run(post):
    request = {
        "url": API_URL,
        "method": "POST",
        "headers": {
            "Authorization": "Bearer ***",
            "Content-Type": "application/json",
        },
        "body": build_payload(post),
    }
    print(json.dumps(request, ensure_ascii=True, indent=2, sort_keys=True))


def run():
    args = parse_args()
    root = repo_root()
    input_path = resolve_path(args.input, pathlib.Path.cwd())
    out_dir = resolve_path(args.out, root)
    posts = read_posts(input_path, args.limit)
    if not posts:
        raise FatalError("Input file has no posts.")

    if args.dry_run:
        if posts[0].get("_read_error"):
            raise FatalError(posts[0]["_read_error"])
        dry_run(posts[0])
        return 0

    api_key = read_api_key()
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / f"results_{args.tag}.jsonl"
    errors_path = out_dir / f"results_{args.tag}.errors.jsonl"
    report_path = out_dir / f"report_{args.tag}.md"
    done_ids = load_existing_ids(results_path)

    results, failures, request_count = load_resume_state(results_path, errors_path)
    posts_by_id = {}
    missing_id_count = 0
    start = time.time()

    for post in posts:
        post_id = str(post.get("id", ""))
        if not post_id:
            missing_id_count += 1
            post_id = f"missing-id-{missing_id_count}"
        posts_by_id.setdefault(post_id, post)
        if post_id in done_ids:
            continue
        if post.get("_read_error"):
            failures += 1
            append_jsonl(errors_path, {"id": post_id, "error": post["_read_error"]})
            continue
        try:
            response, attempts = http_post(build_payload(post), api_key)
            request_count += attempts
            parsed = parse_answer(response, post_id)
            append_jsonl(results_path, parsed)
            results.append(parsed)
            done_ids.add(post_id)
        except FatalError:
            raise
        except Exception as exc:
            failures += 1
            request_count += getattr(exc, "attempts", 0)
            append_jsonl(errors_path, {"id": post_id, "error": str(exc)})

    write_report(
        report_path,
        results,
        failures,
        time.time() - start,
        request_count,
        posts_by_id,
    )
    return 0


def main():
    try:
        return run()
    except FatalError as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
