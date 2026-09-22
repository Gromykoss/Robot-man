#!/usr/bin/env python3
"""Distill Sergey's edits from draft/final pairs with TypeSafe System One Jev."""

import argparse
import datetime
import json
import os
import pathlib
import random
import re
import statistics
import subprocess
import sys
import time
import urllib.request


API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
MAX_ATTEMPTS = 5
TIMEOUT_SECONDS = 30
DEFAULT_SINCE = "2026-09-03"

JUDGMENT_KEYS = [
    "hook_changed",
    "tone_tightened",
    "specificity_added",
    "structure_reordered",
    "length_reduced",
    "length_expanded",
    "cta_changed",
]

SCORE_KEYS = [
    "hook_strength",
    "dwell_potential",
    "reply_potential",
    "profile_click_potential",
    "follow_potential",
]


class FatalError(Exception):
    pass


class SkipPairError(Exception):
    pass


def repo_root():
    return pathlib.Path(__file__).resolve().parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Learn edit patterns by comparing RU drafts, EN finals, and X metrics."
    )
    parser.add_argument(
        "--tag",
        default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        help="Output tag. Default: UTC date YYYY-MM-DD.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means all pairs.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print first request with masked Authorization, then exit.",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not call xurl; use metrics-corpus text as final text.",
    )
    parser.add_argument(
        "--since",
        default=DEFAULT_SINCE,
        help="Only posts created at/after this date enter pairing. Default: 2026-09-03.",
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
                if in_env and line and not line.startswith((" ", "\t")):
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


def parse_datetime(value):
    if not value or not isinstance(value, str):
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def parse_since(value):
    try:
        parsed = datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise FatalError(f"Invalid --since date: {value}") from exc
    return datetime.datetime.combine(
        parsed, datetime.time.min, tzinfo=datetime.timezone.utc
    )


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def extract_metrics(entry):
    nested = entry.get("public_metrics")
    if isinstance(nested, dict):
        source = nested
    else:
        source = entry
    aliases = {
        "impression_count": "impressions",
        "like_count": "likes",
        "reply_count": "replies",
        "retweet_count": "retweets",
        "bookmark_count": "bookmarks",
        "quote_count": "quotes",
    }
    keys = [
        "impression_count",
        "like_count",
        "reply_count",
        "retweet_count",
        "bookmark_count",
        "quote_count",
    ]
    metrics = {}
    for key in keys:
        value = source.get(key)
        if value is None:
            value = source.get(aliases[key])
        if value is None:
            value = 0
        try:
            metrics[key] = int(float(value))
        except (TypeError, ValueError):
            metrics[key] = 0
    return metrics


def load_published_index(root):
    path = root / "published_posts.jsonl"
    index = {}
    if not path.exists():
        return index
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            post_id = item.get("id")
            if post_id is not None and isinstance(item, dict):
                index[str(post_id)] = item
    return index


def load_metrics(root, since_dt):
    published = load_published_index(root)
    posts = {}
    metrics_dir = root / "data" / "metrics"
    for path in sorted(metrics_dir.glob("daily_*.json")):
        data = read_json(path)
        if not isinstance(data, list):
            continue
        for entry in data:
            if not isinstance(entry, dict):
                continue
            post_id = entry.get("id")
            if post_id is None:
                continue
            post_id = str(post_id)
            published_item = published.get(post_id, {})
            created_at_raw = entry.get("created_at") or published_item.get("created_at")
            created_at = parse_datetime(created_at_raw)
            if created_at is None or created_at < since_dt:
                continue
            posts[post_id] = {
                "id": post_id,
                "created_at": created_at,
                "created_at_raw": created_at_raw,
                "text": str(entry.get("text") or published_item.get("text") or ""),
                "metrics": extract_metrics(entry),
            }
    return posts


def draft_topic_match(path):
    return re.match(r"^(?P<topic>.+)_v(?P<version>\d+)_ru\.md$", path.name)


def load_draft_topics(root):
    drafts_dir = root / "drafts"
    topics = {}
    for path in sorted(drafts_dir.glob("*_v*_ru.md")):
        match = draft_topic_match(path)
        if not match:
            continue
        topic = match.group("topic")
        version = int(match.group("version"))
        topics.setdefault(topic, {"ru": [], "en": []})["ru"].append(
            {"path": path, "version": version, "mtime": path.stat().st_mtime}
        )
    for topic, item in topics.items():
        for path in sorted(drafts_dir.glob(f"{topic}*_en.txt")):
            item["en"].append({"path": path, "mtime": path.stat().st_mtime})
        item["ru"].sort(key=lambda row: (row["version"], row["path"].name))
        item["en"].sort(key=lambda row: (row["mtime"], row["path"].name))
        vocab = tokenize(topic.replace("_", " ").replace("-", " "))
        if item["ru"]:
            vocab |= tokenize(item["ru"][0]["path"].read_text(encoding="utf-8", errors="replace")[:120])
        if item["en"]:
            vocab |= tokenize(item["en"][-1]["path"].read_text(encoding="utf-8", errors="replace")[:120])
        item["vocab"] = vocab
    return topics


def tokenize(value):
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "draft",
        "final",
        "post",
        "note",
        "new",
        "our",
        "you",
        "are",
        "was",
        "has",
        "this",
        "that",
        "from",
        "into",
        "over",
        "just",
        "like",
        "have",
        "been",
        "they",
        "when",
        "what",
        "your",
        "not",
        "but",
        "can",
        "all",
        "out",
        "get",
        "one",
        "two",
        "run",
        "use",
        "how",
        "why",
        "its",
        "his",
        "her",
        "him",
        "she",
        "may",
        "via",
        "per",
        "more",
        "most",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) >= 3 and token not in stopwords
    }


def topic_overlaps_text(topic_vocab, text):
    text_tokens = tokenize(text[:500])
    return len(topic_vocab & text_tokens)


def choose_topic(post, topics):
    if post["text"].lstrip().startswith("@"):
        return None, "no_pair"
    candidates = []
    for topic_name, topic in topics.items():
        overlap_count = topic_overlaps_text(topic["vocab"], post["text"])
        if overlap_count >= 2:
            candidates.append((overlap_count, topic_name, topic))
    if not candidates:
        return None, "no_pair"
    max_overlap = max(overlap_count for overlap_count, _, _ in candidates)
    best = [(name, topic) for overlap_count, name, topic in candidates if overlap_count == max_overlap]
    if len(best) != 1:
        return None, "ambiguous"
    return best[0], None


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def fetch_live_final_text(post_id):
    endpoint = f"/2/tweets/{post_id}?tweet.fields=note_tweet,created_at,public_metrics"
    command = [
        "xurl",
        "--app",
        "my-app",
        "--auth",
        "oauth2",
        "-u",
        "@RobotsTJ500",
        endpoint,
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        return None
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    data = payload.get("data")
    if not isinstance(data, dict):
        return None
    note_tweet = data.get("note_tweet")
    if isinstance(note_tweet, dict) and isinstance(note_tweet.get("text"), str):
        return note_tweet["text"]
    text = data.get("text")
    if isinstance(text, str):
        return text
    return None


def build_pairs(root, posts, limit, no_fetch):
    topics = load_draft_topics(root)
    pairs = []
    counts = {"skipped_no_pair": 0, "skipped_ambiguous": 0}
    sorted_posts = sorted(posts.values(), key=lambda post: post["created_at"], reverse=True)
    for post in sorted_posts:
        if limit and len(pairs) >= limit:
            break
        chosen, reason = choose_topic(post, topics)
        if reason == "ambiguous":
            counts["skipped_ambiguous"] += 1
            continue
        if reason == "no_pair" or chosen is None:
            counts["skipped_no_pair"] += 1
            continue
        topic_name, topic = chosen
        if len(topic["ru"]) < 2 or not topic["en"]:
            counts["skipped_no_pair"] += 1
            continue
        draft_first = read_text(topic["ru"][0]["path"])
        draft_last = read_text(topic["ru"][-1]["path"])
        final_text = None if no_fetch else fetch_live_final_text(post["id"])
        if not final_text:
            final_text = post["text"]
        if not final_text:
            counts["skipped_no_pair"] += 1
            continue
        pairs.append(
            {
                "id": post["id"],
                "created_at": post["created_at"],
                "topic": topic_name,
                "draft_first": draft_first,
                "draft_last": draft_last,
                "final_text": final_text,
                "final_candidate": str(topic["en"][-1]["path"]),
                "metrics": post["metrics"],
            }
        )
    return pairs, counts


def compact_state(pair):
    return {
        "draft_first": pair["draft_first"][:1500],
        "draft_last": pair["draft_last"][:1500],
        "final": pair["final_text"][:1500],
    }


def questions():
    return {
        "hook_changed": {
            "type": "noul",
            "instructions": (
                "Compare `draft_last` vs `final`. `draft_first` is context for evolution. "
                "Was the first line of final substantively rewritten vs draft_last?"
            ),
            "criteria": {
                "true": "first line of final is substantively rewritten vs draft_last",
                "false": "hook idea preserved",
            },
        },
        "tone_tightened": {
            "type": "noul",
            "instructions": (
                "Compare `draft_last` vs `final`. Did the final remove hype, marketing, "
                "or ad-flavor present in draft?"
            ),
            "criteria": {
                "true": "final removes hype/marketing/ad-flavor present in draft",
                "false": "tone unchanged or softer hype removed only slightly",
            },
        },
        "specificity_added": {
            "type": "noul",
            "instructions": (
                "Compare `draft_last` vs `final`. Did final add concrete numbers, names, "
                "or steps absent in draft?"
            ),
            "criteria": {
                "true": "final adds concrete numbers, names or steps absent in draft",
                "false": "no added specificity",
            },
        },
        "structure_reordered": {
            "type": "noul",
            "instructions": "Compare `draft_last` vs `final`. Did block order materially change?",
            "criteria": {
                "true": "block/section order materially changed",
                "false": "order preserved",
            },
        },
        "length_reduced": {
            "type": "noul",
            "instructions": "Is `final` at least 20% shorter than `draft_last`?",
            "criteria": {
                "true": "final is at least 20% shorter than draft_last",
                "false": "not materially shorter",
            },
        },
        "length_expanded": {
            "type": "noul",
            "instructions": "Is `final` at least 20% longer than `draft_last`?",
            "criteria": {
                "true": "final is at least 20% longer than draft_last",
                "false": "not materially longer",
            },
        },
        "cta_changed": {
            "type": "noul",
            "instructions": "Compare `draft_last` vs `final`. Was the ending or CTA rewritten?",
            "criteria": {
                "true": "ending or call-to-action rewritten",
                "false": "ending preserved",
            },
        },
        "hook_strength": {
            "type": "score",
            "instructions": (
                "Rate the scroll-stopping power of the FIRST LINE of `final` "
                "for a technically skilled AI-agent-builder audience."
            ),
            "criteria": [
                "scrolls past instantly",
                "weak - generic opener",
                "decent - mild curiosity",
                "strong - specific claim, number or scene in line 1",
                "must-stop - contrarian or concrete result in line 1",
            ],
        },
        "dwell_potential": {
            "type": "score",
            "instructions": (
                "How much of `final` rewards staying and processing "
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
                "How likely does `final` provoke practitioner replies "
                "(open question, contested claim, asks for others' experience)?"
            ),
            "criteria": ["none", "unlikely", "possible", "likely", "very likely"],
        },
        "profile_click_potential": {
            "type": "score",
            "instructions": (
                "Does `final` signal lived credibility that makes a reader check who wrote it?"
            ),
            "criteria": ["none", "weak", "some", "strong", "very strong"],
        },
        "follow_potential": {
            "type": "score",
            "instructions": "Would `final` convert a niche reader into a follower of the author?",
            "criteria": ["no", "weak", "moderate", "strong", "very strong"],
        },
        "format_class": {
            "type": "choice",
            "instructions": "Classify the format of `final`.",
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


def build_payload(pair):
    return {"state": compact_state(pair), "model": MODEL, "questions": questions()}


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
                return json.loads(response_body)
        except Exception as exc:
            code = getattr(exc, "code", None)
            if code == 401:
                raise FatalError("TypeSafe API authentication failed with HTTP 401.") from exc
            if code == 422:
                raise SkipPairError("TypeSafe API rejected the pair with HTTP 422.") from exc
            if code in (429, 529):
                if attempt >= MAX_ATTEMPTS:
                    raise SkipPairError(
                        f"TypeSafe API returned HTTP {code} after {attempt} attempts."
                    ) from exc
                delay = (2 ** attempt) + random.random()
                time.sleep(delay)
                continue
            if code and 500 <= code <= 599:
                if retry_once_done:
                    raise SkipPairError(
                        f"TypeSafe API returned HTTP {code} after retry."
                    ) from exc
                retry_once_done = True
                time.sleep(2 + random.random())
                continue
            raise SkipPairError(f"Request failed: {exc}") from exc


def number(value, default=0.0):
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_answer(response, pair):
    answers = response.get("answers", {})
    usage = response.get("usage", {})
    judgments = {}
    for key in JUDGMENT_KEYS:
        answer = answers.get(key, {})
        judgments[key] = number(answer.get("noul")) >= 0.5

    scores = {}
    for key in SCORE_KEYS:
        answer = answers.get(key, {})
        scores[key] = number(answer.get("score"))

    composite_0_4 = (
        0.30 * scores["hook_strength"]
        + 0.20 * scores["dwell_potential"]
        + 0.20 * scores["reply_potential"]
        + 0.15 * scores["profile_click_potential"]
        + 0.15 * scores["follow_potential"]
    )
    scores["composite_0_4"] = round(composite_0_4, 4)
    scores["composite_0_10"] = round(composite_0_4 * 2.5, 2)

    format_answer = answers.get("format_class", {})
    format_class = str(format_answer.get("choice", "other"))

    return {
        "id": pair["id"],
        "topic": pair["topic"],
        "judgments": judgments,
        "final_scores": scores,
        "format_class": format_class,
        "metrics": pair["metrics"],
        "usage": {
            "input_tokens": int(number(usage.get("input_tokens"), 0)),
            "output_tokens": int(number(usage.get("output_tokens"), 0)),
        },
        "_draft_last_first_line": first_line(pair["draft_last"]),
        "_final_first_line": first_line(pair["final_text"]),
    }


def load_existing_results(path):
    ids = set()
    results = []
    if not path.exists():
        return ids, results
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            post_id = item.get("id")
            if post_id is not None:
                ids.add(str(post_id))
            results.append(item)
    return ids, results


def append_jsonl(path, item):
    with path.open("a", encoding="utf-8") as handle:
        public_item = {key: value for key, value in item.items() if not key.startswith("_")}
        handle.write(json.dumps(public_item, ensure_ascii=True, sort_keys=True) + "\n")


def dry_run(pair):
    request = {
        "url": API_URL,
        "method": "POST",
        "headers": {
            "Authorization": "Bearer ***",
            "Content-Type": "application/json",
        },
        "body": build_payload(pair),
    }
    print(json.dumps(request, ensure_ascii=True, indent=2, sort_keys=True))


def first_line(text):
    for line in str(text).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def truncate_line(text, limit=90):
    text = " ".join(str(text).split()).replace("|", "\\|")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def percent_line(key, results):
    total = len(results)
    if total < 3:
        return f"- {key}: мало данных"
    true_count = sum(1 for item in results if item.get("judgments", {}).get(key))
    share = round((true_count / total) * 100)
    return f"- {key}: {share}% ({true_count}/{total})"


def pick_hook_example(results):
    candidates = []
    for item in results:
        if not item.get("judgments", {}).get("hook_changed"):
            continue
        before = item.get("_draft_last_first_line", "")
        after = item.get("_final_first_line", "")
        if not before or not after or before == after:
            continue
        score = abs(len(after) - len(before)) + len(set(tokenize(after)) ^ set(tokenize(before)))
        candidates.append((score, before, after))
    if not candidates:
        return "", ""
    _, before, after = sorted(candidates, key=lambda row: row[0], reverse=True)[0]
    return truncate_line(before), truncate_line(after)


def add_threshold_rule(lines, key, results, template):
    total = len(results)
    if total < 3:
        return False
    true_count = sum(1 for item in results if item.get("judgments", {}).get(key))
    if true_count / total < 0.5:
        return False
    lines.append(template(true_count, total))
    return True


def metric_value(item, key):
    metrics = item.get("metrics")
    if not isinstance(metrics, dict):
        return 0
    try:
        return int(metrics.get(key, 0))
    except (TypeError, ValueError):
        return 0


def write_voice_lessons(path, results, counts, since_dt):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    created_dates = sorted(
        {
            str(item.get("_created_at", ""))[:10]
            for item in results
            if item.get("_created_at")
        }
    )
    if created_dates:
        date_range = f"{created_dates[0]}..{created_dates[-1]}"
    else:
        date_range = f"{since_dt.date()}..n/a"

    lines = [
        "# VOICE LESSONS — @RobotsTJ500",
        "",
        f"Generated: {now}",
        f"Pairs analyzed: {len(results)}",
        (
            "Skipped: "
            f"no_pair={counts.get('skipped_no_pair', 0)}, "
            f"ambiguous={counts.get('skipped_ambiguous', 0)}"
        ),
        f"Date range: {date_range}",
        "",
        "## Правки Сергея — статистика",
    ]
    for key in JUDGMENT_KEYS:
        lines.append(percent_line(key, results))

    lines.extend(["", "## Правила"])
    rule_lines = []
    before, after = pick_hook_example(results)
    fired = add_threshold_rule(
        rule_lines,
        "hook_changed",
        results,
        lambda n, m: (
            "Хук переписывается чаще всего — первое место правок. "
            f"Пример (draft_last -> final): {before} -> {after} ({n} из {m})"
        ),
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "tone_tightened",
            results,
            lambda n, m: (
                "Финал всегда суше драфта: рекламные эпитеты и хайп убираются. "
                f"Правь в эту сторону до показа Сергею. ({n} из {m})"
            ),
        )
        or fired
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "specificity_added",
            results,
            lambda n, m: (
                "Добавляй конкретику сразу: цифры, имена, шаги — Сергей добавляет "
                f"их вручную. ({n} из {m} правок)"
            ),
        )
        or fired
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "length_reduced",
            results,
            lambda n, m: f"Сокращай: финал короче драфта в большинстве правок. ({n} из {m})",
        )
        or fired
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "length_expanded",
            results,
            lambda n, m: f"Разверни недосказанное: финалы длиннее драфтов. ({n} из {m})",
        )
        or fired
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "structure_reordered",
            results,
            lambda n, m: (
                "Переставляй блоки к порядку: суть -> механика -> опыт -> вывод. "
                f"({n} из {m})"
            ),
        )
        or fired
    )
    fired = (
        add_threshold_rule(
            rule_lines,
            "cta_changed",
            results,
            lambda n, m: (
                "Финал/CTA — второе место правок, пиши его в последнюю очередь и "
                f"предлагай 2 варианта. ({n} из {m})"
            ),
        )
        or fired
    )
    if fired:
        lines.extend(rule_lines[:12])
    else:
        lines.append("Правок пока мало — правил не выведено.")

    lines.extend(["", "## Метрика"])
    composites = [
        item.get("final_scores", {}).get("composite_0_10", 0)
        for item in results
    ]
    mean_composite = round(statistics.mean(composites), 2) if composites else 0.0
    lines.append(f"- mean composite_0_10: {mean_composite}")
    if results:
        best = max(results, key=lambda item: item.get("final_scores", {}).get("composite_0_10", 0))
        worst = min(results, key=lambda item: item.get("final_scores", {}).get("composite_0_10", 0))
        lines.append(
            "- best post: "
            f"{best.get('id')} + {best.get('topic')} + "
            f"{best.get('final_scores', {}).get('composite_0_10', 0)} + "
            f"{metric_value(best, 'impression_count')} impressions"
        )
        lines.append(
            "- worst post: "
            f"{worst.get('id')} + {worst.get('topic')} + "
            f"{worst.get('final_scores', {}).get('composite_0_10', 0)} + "
            f"{metric_value(worst, 'impression_count')} impressions"
        )
    else:
        lines.append("- best post: n/a")
        lines.append("- worst post: n/a")

    lines.extend(["", "Обновляется прогоном: python3 scripts/jev_edit_learner.py"])
    path.write_text("\n".join(lines[:120]) + "\n", encoding="utf-8")


def public_result_with_context(parsed, pair):
    parsed["_created_at"] = pair["created_at"].date().isoformat()
    return parsed


def run():
    args = parse_args()
    root = repo_root()
    since_dt = parse_since(args.since)
    posts = load_metrics(root, since_dt)
    if not posts:
        raise FatalError("No metrics posts found at/after --since.")

    start = time.time()
    pairs, counts = build_pairs(root, posts, args.limit, args.no_fetch)
    if not pairs:
        raise FatalError(
            "No eligible draft/final pairs found after deterministic pairing."
        )

    if args.dry_run:
        dry_run(pairs[0])
        return 0

    api_key = read_api_key()
    out_dir = root / "data" / "learning"
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / f"edit_patterns_{args.tag}.jsonl"
    errors_path = out_dir / f"edit_patterns_{args.tag}.errors.jsonl"
    done_ids, results = load_existing_results(results_path)
    request_count = 0
    failures = 0

    enriched_by_id = {str(item.get("id")): item for item in results}
    for pair in pairs:
        post_id = str(pair["id"])
        if post_id in done_ids:
            existing = enriched_by_id.get(post_id)
            if existing is not None:
                existing["_created_at"] = pair["created_at"].date().isoformat()
            continue
        try:
            response = http_post(build_payload(pair), api_key)
            request_count += 1
            parsed = public_result_with_context(parse_answer(response, pair), pair)
            append_jsonl(results_path, parsed)
            results.append(parsed)
            done_ids.add(post_id)
        except FatalError:
            raise
        except Exception as exc:
            failures += 1
            append_jsonl(errors_path, {"id": post_id, "topic": pair["topic"], "error": str(exc)})

    write_voice_lessons(root / "VOICE_LESSONS.md", results, counts, since_dt)
    total_input = sum(item.get("usage", {}).get("input_tokens", 0) for item in results)
    total_output = sum(item.get("usage", {}).get("output_tokens", 0) for item in results)
    print(
        "summary: "
        f"analyzed={len(results)} "
        f"skipped_no_pair={counts.get('skipped_no_pair', 0)} "
        f"skipped_ambiguous={counts.get('skipped_ambiguous', 0)} "
        f"failures={failures} "
        f"requests={request_count} "
        f"tokens_total={total_input + total_output} "
        f"wall_time={round(time.time() - start, 2)}s"
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
