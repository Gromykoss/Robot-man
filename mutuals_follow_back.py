#!/usr/bin/env python3
"""Follow-back mutuals who follow @RobotsTJ500.

X Algorithm July 2026: mutuals boost — mutual follows get priority in For You + replies.
This script checks who follows @RobotsTJ500 and follows them back.

Dry-run is default. Follow side effects require --execute.
Max 3 follows/day to stay within rate limits.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "data" / "mutuals_log.jsonl"
ACCOUNT = "RobotsTJ500"
APP = "my-app"
AUTH = "oauth1"
MAX_FOLLOWS = 3
DRY_RUN = True


def xurl(*args: str) -> dict:
    """Run xurl CLI and return JSON response."""
    cmd = ["xurl", "--app", APP, "--auth", AUTH, "-u", f"@{ACCOUNT}"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stderr or result.stdout, "raw": result.stdout}


def get_followers() -> list[str]:
    """Get list of follower IDs."""
    data = xurl("followers", "-n", "50")
    followers = []
    if "data" in data:
        for f in data["data"]:
            followers.append(f.get("id") or f.get("user_id") or "")
    return [f for f in followers if f]


def get_following() -> list[str]:
    """Get list of accounts we follow."""
    data = xurl("following", "-n", "50")
    following = []
    if "data" in data:
        for f in data["data"]:
            following.append(f.get("id") or f.get("user_id") or "")
    return [f for f in following if f]


def follow_user(user_id: str, user_name: str = "") -> dict:
    """Follow a user by ID."""
    return xurl("follow", user_id)


def log_action(user_id: str, user_name: str, action: str, result: dict) -> None:
    """Log follow-back action to JSONL."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "user_name": user_name,
        "action": action,
        "result": result,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Follow-back mutuals for @RobotsTJ500")
    parser.add_argument("--execute", action="store_true", help="Actually follow (default: dry-run)")
    parser.add_argument("--limit", type=int, default=MAX_FOLLOWS, help=f"Max follows per run (default: {MAX_FOLLOWS})")
    args = parser.parse_args()

    execute = args.execute
    limit = min(args.limit, MAX_FOLLOWS)

    print(f"[MUTUALS] {'EXECUTE' if execute else 'DRY-RUN'} mode, limit={limit}")

    followers = get_followers()
    following = get_following()

    if not followers:
        print("[MUTUALS] No followers found. Check xurl auth.")
        sys.exit(1)

    print(f"[MUTUALS] Followers: {len(followers)}, Following: {len(following)}")

    missing = [f for f in followers if f not in following]
    print(f"[MUTUALS] Not following back: {len(missing)}")

    if not missing:
        print("[MUTUALS] All followers are mutuals already.")
        return

    # Follow the missing ones
    followed = 0
    for user_id in missing[:limit]:
        action = "dry-run" if not execute else "follow"
        result = {}
        if execute:
            result = follow_user(user_id)
            print(f"  ✓ Followed {user_id}: {result.get('data', result.get('error', 'ok'))}")
        else:
            print(f"  ○ Would follow: {user_id}")
        log_action(user_id, "", action, result)
        followed += 1

    print(f"[MUTUALS] Processed: {followed}/{limit}")


if __name__ == "__main__":
    main()
