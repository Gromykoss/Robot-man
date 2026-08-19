#!/usr/bin/env python3
"""
⛔ DEPRECATED (18.08.2026) — мёртвый рудимент, НЕ использовать.

Этот скрипт НЕ является рабочим фетчером. Реальный фетчер cron:
  ~/.hermes/scripts/x_tracker_fetch.py  (v3.0, twitter CLI → hermes-vault/40_Research/X Tracked/)

Старая схема (tracked_authors.txt → data/tracked_posts.json) заброшена:
  - скрипт никем не вызывается
  - data/tracked_posts.json никем не читается
  - cron cd9bc007c07a работает через ~/.hermes/scripts/x_tracker_fetch.py v3.0

Оставлен только для git-истории. Править фетчер → только ~/.hermes/scripts/x_tracker_fetch.py.

--- исходный docstring (для истории) ---
x_tracker_fetch.py — Fetch latest posts from tracked X accounts via twitter CLI.
Reads /home/hermes-workspace/robot-man/tracked_authors.txt, fetches recent posts,
outputs JSON and saves to data/tracked_posts.json.

Usage:
  python3 x_tracker_fetch.py                    # Normal run
  python3 x_tracker_fetch.py --max 5            # Max tweets per author
  python3 x_tracker_fetch.py --verbose          # Verbose output
  python3 x_tracker_fetch.py --dry-run          # Don't save, just print JSON

Cron: 0 12 * * *   python3 x_tracker_fetch.py
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────
HOME = os.environ.get("HOME", "/home/hermes-workspace")
ROOT = Path(__file__).resolve().parent  # robot-man/
TRACKED_FILE = ROOT / "tracked_authors.txt"
OUTPUT_FILE = ROOT / "data" / "tracked_posts.json"

# twitter CLI is in the Hermes agent venv
TWITTER_BIN = str(
    Path(HOME) / ".hermes" / "hermes-agent" / "venv" / "bin" / "twitter"
)
DEFAULT_MAX = 5  # tweets per author


# ── Helpers ──────────────────────────────────────────────────────────

def load_tracked_authors(path: Path) -> list[str]:
    """Read tracked_authors.txt, return list of usernames (without @)."""
    if not path.exists():
        print(f"[ERROR] Tracked file not found: {path}", file=sys.stderr)
        sys.exit(1)

    authors = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            # Skip comments, empty lines, and lines with metadata separators
            if not line or line.startswith("#"):
                continue
            # Format: "username | reason | priority"
            # Also handle old format: just "username"
            username = line.split("|")[0].strip()
            if username:
                authors.append(username)
    return authors


def twitter_search_from(username: str, max_tweets: int = DEFAULT_MAX) -> dict | None:
    """Run `twitter search --from <username> --max N --json` and return parsed JSON."""
    cmd = [
        TWITTER_BIN, "search", "--from", username,
        "--max", str(max_tweets), "--json",
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=45,
            env={**os.environ, "HOME": HOME},
        )
        if result.returncode != 0:
            print(
                f"[WARN] twitter CLI error for @{username}: {result.stderr.strip()[:200]}",
                file=sys.stderr,
            )
            return None
        data = json.loads(result.stdout)
        return data
    except subprocess.TimeoutExpired:
        print(f"[WARN] Timeout fetching @{username}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"[WARN] Invalid JSON from twitter for @{username}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[WARN] Error fetching @{username}: {e}", file=sys.stderr)
        return None


def extract_posts(data: dict, tracked_username: str) -> list[dict]:
    """Extract posts from twitter search result, filtering by exact author match."""
    if not data or not data.get("ok"):
        return []

    tweets = data.get("data", [])
    if not isinstance(tweets, list):
        return []

    posts = []
    for t in tweets:
        author = t.get("author", {})
        screen_name = author.get("screenName", "")
        # Filter: only keep tweets where author matches the tracked username
        # (twitter search --from is fuzzy, may return other users)
        if screen_name.lower() != tracked_username.lower():
            continue

        post = {
            "author": screen_name,
            "tweet_id": t.get("id", ""),
            "text": t.get("text", ""),
            "created_at": t.get("createdAtISO", ""),
        }
        posts.append(post)

    return posts


def build_output(all_posts: list[dict]) -> dict:
    """Build final output dict with metadata."""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "posts": all_posts,
    }


def save_output(data: dict, path: Path) -> None:
    """Save JSON to file, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved {data['total_posts']} posts to {path}")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch latest posts from tracked X accounts")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX,
                        help=f"Max tweets per author (default: {DEFAULT_MAX})")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print JSON only, don't save to file")
    args = parser.parse_args()

    # 1. Load tracked authors
    authors = load_tracked_authors(TRACKED_FILE)
    if args.verbose:
        print(f"[INFO] Loaded {len(authors)} tracked authors: {', '.join(authors[:20])}")

    # 2. Fetch posts for each author
    all_posts_by_author = []
    errors = []

    for username in authors:
        if args.verbose:
            print(f"[INFO] Fetching @{username} ({args.max} tweets)...")

        data = twitter_search_from(username, args.max)

        if data is None:
            errors.append({"author": username, "error": "twitter_cli_failed"})
            continue

        if not data.get("ok"):
            errors.append({"author": username, "error": f"twitter_api: {data.get('error', 'unknown')}"})
            continue

        posts = extract_posts(data, username)
        all_posts_by_author.extend(posts)

        if args.verbose:
            print(f"[INFO]   @{username}: {len(posts)} posts")

    # 3. Build output
    output = build_output(all_posts_by_author)
    if errors:
        output["errors"] = errors

    # 4. Print JSON to stdout
    json_out = json.dumps(output, indent=2, ensure_ascii=False)
    print(json_out)

    # 5. Save to file (unless dry-run)
    if not args.dry_run:
        save_output(output, OUTPUT_FILE)

    # Exit with error if all authors failed
    if errors and not all_posts_by_author:
        print(f"[ERROR] All {len(authors)} authors failed. Check twitter CLI auth.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
