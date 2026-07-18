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


def xurl_oauth2(url: str) -> dict:
    """Run xurl with OAuth2 for read operations."""
    cmd = ["xurl", "--app", APP, "--auth", "oauth2", "-u", f"@{ACCOUNT}", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stderr or result.stdout}


def get_followers() -> list[str]:
    """Get all follower IDs with pagination."""
    all_followers = []
    next_token = None
    for _ in range(5):  # Max 5 pages = 1000 followers
        url = f"/2/users/1880157852632772608/followers?max_results=200&user.fields=id,username"
        if next_token:
            url += f"&pagination_token={next_token}"
        data = xurl_oauth2(url)
        users = data.get("data", [])
        all_followers.extend(u.get("id") or u.get("user_id") or "" for u in users)
        next_token = data.get("meta", {}).get("next_token")
        if not next_token:
            break
    return [f for f in all_followers if f]


def get_following() -> list[str]:
    """Get list of accounts we follow."""
    data = xurl("following", "-n", "50")
    following = []
    if "data" in data:
        for f in data["data"]:
            following.append(f.get("id") or f.get("user_id") or "")
    return [f for f in following if f]


def follow_user(user_id: str) -> dict:
    """Follow a user. Resolves ID → username first (xurl expects username)."""
    profile = fetch_user_profile(user_id)
    username = profile.get("username", "")
    if not username:
        return {"error": "no_username", "user_id": user_id}
    return xurl("follow", username)


def fetch_user_profile(user_id: str) -> dict:
    """Fetch user profile details for quality check."""
    result = subprocess.run(
        ["xurl", "--app", APP, "--auth", "oauth2", "-u", f"@{ACCOUNT}",
         f"/2/users/{user_id}?user.fields=description,public_metrics,created_at,verified"],
        capture_output=True, text=True, timeout=15,
    )
    try:
        data = json.loads(result.stdout)
        return (data.get("data") or {})
    except (json.JSONDecodeError, KeyError):
        return {}


def should_follow(user_id: str) -> tuple[bool, str]:
    """Quality gate: skip dormant, fresh, spammy accounts."""
    profile = fetch_user_profile(user_id)
    if not profile:
        return False, "no_profile"

    metrics = profile.get("public_metrics", {})
    tweet_count = metrics.get("tweet_count", 0)
    followers_count = metrics.get("followers_count", 0)
    created_at = profile.get("created_at", "")

    if tweet_count == 0:
        return False, "zero_tweets"
    if tweet_count < 5 and followers_count < 10:
        return False, "dormant"
    if created_at > "2026-06-15":
        return False, "too_new"
    if not profile.get("description"):
        return False, "no_bio"

    return True, "ok"


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

    # Follow the missing ones (with quality gate)
    followed = 0
    skipped = 0
    for user_id in missing:
        if followed >= limit:
            break
        
        ok, reason = should_follow(user_id)
        if not ok:
            print(f"  ✗ Skip {user_id}: {reason}")
            log_action(user_id, "", f"skip:{reason}", {})
            skipped += 1
            continue

        action = "dry-run" if not execute else "follow"
        result = {}
        if execute:
            result = follow_user(user_id)
            print(f"  ✓ Followed {user_id}: {result.get('data', result.get('error', 'ok'))}")
        else:
            print(f"  ○ Would follow: {user_id} (quality: {reason})")
        log_action(user_id, "", action, result)
        if execute and not result.get("error"):
            followed += 1
        elif not execute:
            followed += 1
        else:
            print(f"  ✗ Follow failed: {result.get('error')}")

    print(f"[MUTUALS] Followed: {followed}/{limit}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
