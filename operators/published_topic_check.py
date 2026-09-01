"""Check recently published posts against a draft topic — dedupe gate for content jobs.

Usage: python3 published_topic_check.py "draft topic keywords"
Exit 0 = no recent overlap, safe to draft.
Exit 2 = overlap detected with a post published in the last N days (default 7).
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
PUBLISHED_LOG = PROJECT / "published_posts.jsonl"
WINDOW_DAYS = 7
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at", "by",
        "is", "are", "was", "were", "it", "its", "we", "our", "i", "my", "me", "you", "your"}


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zа-я0-9]{4,}", text.lower()) if w not in STOP}


def fetch_post_texts(ids: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pid in ids:
        try:
            r = subprocess.run(
                ["xurl", "/2/tweets/" + pid],
                capture_output=True, text=True, timeout=30,
            )
            d = json.loads(r.stdout)
            out[pid] = d["data"]["text"].lower()
        except Exception:
            pass
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: published_topic_check.py 'topic keywords'")
        return 1
    draft_tokens = tokens(" ".join(sys.argv[1:]))
    if not draft_tokens:
        print("no meaningful tokens in query")
        return 1

    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    recent: list[str] = []
    for line in PUBLISHED_LOG.read_text().splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = rec.get("created_at") or rec.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt >= cutoff:
            recent.append(rec["id"])

    if not recent:
        print("OK: no posts published in the last", WINDOW_DAYS, "days")
        return 0

    texts = fetch_post_texts(recent)
    flagged = []
    for pid, text in texts.items():
        overlap = draft_tokens & tokens(text)
        if len(overlap) >= 3:
            flagged.append((pid, sorted(overlap)))

    if flagged:
        print("DUPLICATE RISK — draft topic overlaps recent published posts:")
        for pid, words in flagged:
            print(f"  {pid}: shared keywords {words}")
        print("=> Do NOT draft this topic. Pick another from CONTENT_BRIEF or report.")
        return 2
    print("OK: no significant overlap with", len(recent), "recent posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
