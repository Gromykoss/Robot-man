#!/usr/bin/env python3
"""Dialogue watchdog: @catmanyau thread under AI Village post 2093630797202723130.
State-based: exits 0 silently when nothing new (no_change tick); emits DIALOG_UPDATE
marker when catmanyau replied to our latest message. Max 5 bot replies enforced via state file."""
import json, os, sys, subprocess, datetime

POST = "2093630797202723130"
CAT_ID = "1439593236457218054"
STATE = os.path.expanduser("~/robot-man/data/dialog_catmanyau_state.json")
MAX_REPLIES = 5

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"bot_replies": 1, "last_seen_reply_id": "2093657757622681807", "closed": False}

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"), indent=1)

def xurl(path):
    r = subprocess.run(["xurl", "--app", "my-app", "--auth", "oauth1", path],
                       capture_output=True, text=True, timeout=60)
    raw = r.stdout
    first = raw.find("{")
    if first < 0:
        return {}
    depth, end = 0, first
    for i, c in enumerate(raw[first:], first):
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: end = i + 1; break
    try:
        return json.loads(raw[first:end])
    except Exception:
        return {}

s = load_state()
if s.get("closed"):
    print("DIALOG_CLOSED max bot replies reached, watchdog exiting")
    save_state({**s, "closed": True})
    sys.exit(0)

d = xurl(f"/2/tweets/search/recent?query=conversation_id%3A{POST}&max_results=20&tweet.fields=author_id,created_at")
if not d:
    print("API_ERROR: search failed (402/503/empty response) - state unchanged, will retry next tick")
    sys.exit(0)
replies = [t for t in d.get("data", []) if t.get("author_id") == CAT_ID]
replies.sort(key=lambda t: int(t["id"]))
newest = replies[-1]["id"] if replies else None

last_seen = s.get("last_seen_reply_id", "0")
if not newest or int(newest) <= int(last_seen):
    save_state(s)  # persist baseline even when silent
    sys.exit(0)  # nothing new -> silent no_change tick

new_replies = [t for t in replies if int(t["id"]) > int(last_seen)]
latest = new_replies[-1]
print("DIALOG_UPDATE")
print("from: @catmanyau, id:", latest["id"])
print("text:", latest["text"][:600])
print("new_replies_count:", len(new_replies))
print("bot_replies_used:", s.get("bot_replies", 1), "/", MAX_REPLIES)
if s.get("bot_replies", 1) >= MAX_REPLIES:
    print("LIMIT_REACHED: do not reply further — close dialog politely or let it rest")
save_state({**s, "last_seen_reply_id": newest})
