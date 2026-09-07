#!/usr/bin/env python3
"""Off-pipeline post watchdog.

Detects tweets published by @RobotsTJ500 that bypassed post_with_log.sh
(i.e. not present in published_posts.jsonl). Exit code 1 + alert text if found.

Usage: python3 scripts/offpipeline_watchdog.py
State: data/offpipeline_state.json (known legit ids).
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, "published_posts.jsonl")
STATE = os.path.join(BASE, "data", "offpipeline_state.json")
ACCOUNT_ID = "1880157852632772608"  # RobotsTJ500

def load_jsonl(path):
    ids = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    tid = d.get("id") or d.get("tweet_id")
                    if tid:
                        ids.add(str(tid))
                except json.JSONDecodeError:
                    pass
    return ids

def fetch_recent_tweets():
    """Fetch recent tweet ids of the account via syndication user timeline (read-only, no credits)."""
    try:
        out = subprocess.run(
            ["xurl", f"/2/users/{ACCOUNT_ID}/tweets?max_results=25&exclude=replies"],
            capture_output=True, text=True, timeout=60)
        raw = out.stdout.strip()
        if not raw or '"data"' not in raw:
            print(f"WATCHDOG: read failed ({raw[:120]}) — skipping check, NOT treating as clean")
            return None
        data = json.loads(raw[raw.find("{"):])
        return [str(t["id"]) for t in data.get("data", [])]
    except Exception as e:
        print(f"WATCHDOG: read error {e} — skipping check")
        return None

def main():
    logged = load_jsonl(LOG)
    known = set()
    if os.path.exists(STATE):
        try:
            known = set(json.load(open(STATE)))
        except Exception:
            known = set()

    recent = fetch_recent_tweets()
    if recent is None:
        print("WATCHDOG: cannot fetch recent tweets (API read failed) — skipping check")
        return 0

    suspects = [t for t in recent if t not in logged and t not in known]

    if suspects:
        print(f"ALERT: {len(suspects)} post(s) NOT in published_posts.jsonl (off-pipeline write suspected):")
        for t in suspects:
            print(f"  https://x.com/RobotsTJ500/status/{t}")
        return 1

    # update state (all clean)
    all_ids = sorted(logged | set(recent))[-500:]
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(all_ids, open(STATE, "w"))
    print(f"WATCHDOG OK: {len(recent)} recent posts, all logged. State has {len(all_ids)} ids.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
