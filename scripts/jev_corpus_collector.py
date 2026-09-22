#!/usr/bin/env python3
"""Collect a recent X corpus for JEV viral analysis."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


QUERIES = [
    '("AI agent" OR "AI agents" OR "coding agent") -is:retweet -is:reply lang:en',
    '("coding agents") -is:retweet -is:reply lang:en',
    '("agent framework" OR "MCP server" OR "LLM agent") -is:retweet -is:reply lang:en',
    '("autonomous agent" OR "AI agents") -is:retweet -is:reply lang:en',
    '("building in public") (AI OR agent) -is:retweet -is:reply lang:en',
    '("Claude Code" OR "Codex CLI") -is:retweet -is:reply lang:en',
    '("multi-agent" OR "agent swarm") -is:retweet -is:reply lang:en',
    '("agentic" OR "AI workflow") -is:retweet -is:reply lang:en',
    '("prompt engineering" OR "context engineering") -is:retweet -is:reply lang:en',
    '("agent skills" OR "AI memory" OR "agent loop") -is:retweet -is:reply lang:en',
]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tag",
        default=datetime.now(timezone.utc).strftime("%Y%m%d"),
        help="Output file suffix, defaults to today's UTC date.",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run one query and one page only.",
    )
    parser.add_argument(
        "--out",
        default="data/jev_viral_analysis",
        help="Output directory, relative to repo root unless absolute.",
    )
    return parser.parse_args()


def output_dir(raw_out: str) -> Path:
    path = Path(raw_out)
    if not path.is_absolute():
        path = repo_root() / path
    return path


def xurl_recent_search(query: str, next_token: str | None) -> dict | None:
    params = {
        "query": query,
        "max_results": "100",
        "tweet.fields": "public_metrics,created_at,note_tweet",
        "expansions": "author_id",
        "user.fields": "public_metrics,username",
    }
    if next_token:
        params["next_token"] = next_token
    cmd = ["xurl", f"/2/tweets/search/recent?{urlencode(params)}"]

    try:
        proc = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
    except subprocess.TimeoutExpired:
        print(f"xurl timeout query={query!r}", file=sys.stderr)
        return None
    except OSError as exc:
        print(f"xurl failed query={query!r}: {exc}", file=sys.stderr)
        return None

    if proc.returncode != 0:
        print(f"xurl exit={proc.returncode} query={query!r}", file=sys.stderr)
        if proc.stderr:
            print(proc.stderr.strip(), file=sys.stderr)
        return None

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(f"xurl invalid json query={query!r}: {exc}", file=sys.stderr)
        return None

    if isinstance(payload, dict) and ("error" in payload or ("errors" in payload and "data" not in payload)):
        print(f"xurl error object query={query!r}: {json.dumps(payload, ensure_ascii=True)}", file=sys.stderr)
        return None

    if not isinstance(payload, dict):
        print(f"xurl unexpected response query={query!r}", file=sys.stderr)
        return None

    return payload


def user_index(payload: dict) -> dict[str, dict]:
    users = payload.get("includes", {}).get("users", [])
    if not isinstance(users, list):
        return {}
    return {str(user.get("id")): user for user in users if isinstance(user, dict) and user.get("id")}


def post_from_tweet(tweet: dict, users_by_id: dict[str, dict]) -> dict:
    author_id = str(tweet.get("author_id", ""))
    author = users_by_id.get(author_id, {})
    author_metrics = author.get("public_metrics") if isinstance(author.get("public_metrics"), dict) else {}
    text = tweet.get("text", "")
    note_tweet = tweet.get("note_tweet")
    if isinstance(note_tweet, dict) and note_tweet.get("text"):
        text = note_tweet["text"]

    metrics = tweet.get("public_metrics")
    if not isinstance(metrics, dict):
        metrics = {}

    return {
        "id": str(tweet.get("id", "")),
        "text": text,
        "author": author.get("username", ""),
        "author_followers": author_metrics.get("followers_count", 0),
        "metrics": metrics,
        "created_at": tweet.get("created_at", ""),
    }


def is_viral(post: dict) -> bool:
    metrics = post.get("metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}
    text = post.get("text", "")
    return (
        len(text) >= 80
        and (
            int(metrics.get("impression_count") or 0) >= 3000
            or int(metrics.get("like_count") or 0) >= 15
            or int(metrics.get("bookmark_count") or 0) >= 15
        )
    )


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def collect(smoke: bool) -> tuple[list[dict], int, int]:
    selected_queries = QUERIES[:1] if smoke else QUERIES
    max_pages = 1 if smoke else 3
    posts_by_id: dict[str, dict] = {}
    ok_queries = 0

    for query in selected_queries:
        query_ok = False
        next_token: str | None = None
        for _page in range(max_pages):
            payload = xurl_recent_search(query, next_token)
            if payload is None:
                break
            query_ok = True

            users_by_id = user_index(payload)
            data = payload.get("data", [])
            if isinstance(data, list):
                for tweet in data:
                    if not isinstance(tweet, dict) or not tweet.get("id"):
                        continue
                    post = post_from_tweet(tweet, users_by_id)
                    posts_by_id.setdefault(post["id"], post)

            meta = payload.get("meta", {})
            if not isinstance(meta, dict):
                break
            next_token = meta.get("next_token")
            if not next_token:
                break

        if query_ok:
            ok_queries += 1

    return list(posts_by_id.values()), ok_queries, len(selected_queries)


def main() -> int:
    args = parse_args()
    out_dir = output_dir(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_posts, ok_queries, total_queries = collect(args.smoke)
    viral_posts = [post for post in raw_posts if is_viral(post)]

    write_jsonl(out_dir / f"corpus_{args.tag}_raw.jsonl", raw_posts)
    write_jsonl(out_dir / f"corpus_{args.tag}_run.jsonl", viral_posts)

    print(f"COLLECTED raw={len(raw_posts)} viral={len(viral_posts)} queries={ok_queries}/{total_queries} tag={args.tag}")

    min_raw = 5 if args.smoke else 50
    if ok_queries >= 1 and len(raw_posts) >= min_raw:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
