#!/usr/bin/env python3
"""Watchdog: уведомить Сергея, когда кто-то ответит на реплай @RobotsTJ500 к @KSimback.

Тихий (пустой stdout), когда ничего нового. Печатает русское уведомление,
когда появляется НОВЫЙ ответ на наш реплай. Дедупликация через state-файл.

Запуск как no_agent cron-watchdog: каждый тик; пустой stdout = молчать.
"""
import json
import os
import subprocess

POST_ID = "2088645305311154504"          # наш реплай @RobotsTJ500
CONVERSATION_ID = "2088609838943162571"  # корень треда (пост Кевина)
POST_URL = f"https://x.com/RobotsTJ500/status/{POST_ID}"
STATE_PATH = "/home/hermes-workspace/robot-man/data/ksimback_reply_state.json"


def xurl_json(args):
    try:
        out = subprocess.run(
            ["xurl"] + args, capture_output=True, text=True, timeout=45
        )
        if out.returncode != 0 or not out.stdout.strip():
            return None
        dec = json.JSONDecoder()
        data, _ = dec.raw_decode(out.stdout)
        return data
    except Exception:
        return None


def load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"seen_reply_ids": []}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f)


def fetch_replies_to_our_post():
    """Список {id, author, text} для ответов напрямую на наш реплай."""
    q = f"conversation_id:{CONVERSATION_ID}"
    res = xurl_json([
        "/2/tweets/search/recent",
        f"query={q}",
        "tweet.fields=author_id,created_at,referenced_tweets",
        "expansions=author_id",
        "user.fields=username,name",
        "max_results=100",
    ])
    if not res:
        return None
    users = {u["id"]: u.get("username", "?") for u in res.get("includes", {}).get("users", [])}
    replies = []
    for t in res.get("data", []):
        if t.get("id") == POST_ID:
            continue
        refs = t.get("referenced_tweets", [])
        is_reply_to_us = any(
            r.get("type") == "replied_to" and r.get("id") == POST_ID for r in refs
        )
        if not is_reply_to_us:
            continue
        replies.append({
            "id": t.get("id"),
            "author": users.get(t.get("author_id"), "?"),
            "text": (t.get("text") or "").strip(),
        })
    return replies


def main():
    post = xurl_json(["read", POST_ID])
    if post is None:
        return  # не смогли прочитать — молчим, не спамим ошибками
    pm = post.get("data", {}).get("public_metrics", {})
    reply_count = pm.get("reply_count", 0)

    if reply_count == 0:
        return  # тихо

    state = load_state()
    seen = set(state.get("seen_reply_ids", []))

    replies = fetch_replies_to_our_post()
    if replies is None:
        # reply_count > 0, но детали не загрузились — уведомить один раз по счётчику
        if state.get("last_reply_count") != reply_count:
            state["last_reply_count"] = reply_count
            save_state(state)
            print(
                f"✉️ На твой реплай @KSimback кто-то ответил "
                f"(reply_count={reply_count}), но детали не загрузились. "
                f"Проверь: {POST_URL}"
            )
        return

    new_replies = [r for r in replies if r["id"] not in seen]
    if not new_replies:
        return  # тихо, нового нет

    for r in new_replies:
        seen.add(r["id"])
    state["seen_reply_ids"] = sorted(seen)
    state["last_reply_count"] = reply_count
    save_state(state)

    for r in new_replies:
        print(
            f"✉️ Ответ на твой реплай от @{r['author']}:\n"
            f"{r['text']}\n"
            f"Ссылка: https://x.com/{r['author']}/status/{r['id']}\n"
        )


if __name__ == "__main__":
    main()
