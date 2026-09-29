#!/usr/bin/env bash
# UCP-пост 2104889500472115551: наблюдение 12ч, интервал 30 мин (29.09).
# Лог + уведомление только при изменениях. Джобу удалит отчётный запуск после 12ч.
set -u
POST_ID=2104889500472115551
DIR=/home/hermes-workspace/robot-man
LOG=$DIR/logs/ucp_post_watch.log
mkdir -p "$DIR/logs"
NOW=$(date -u +%FT%R)
START=2026-09-29T11:35

# Стоп через 12ч: удалить джобу и зафиксировать финал
if [ "$(date -u +%s)" -ge "$(( $(date -u -d "$START" +%s) + 43200 ))" ]; then
  xurl --app my-app --auth oauth2 -u RobotsTJ500 "/2/tweets/$POST_ID?tweet.fields=public_metrics" 2>/dev/null \
    | grep -o '"impression_count":[0-9]*\|"like_count":[0-9]*\|"reply_count":[0-9]*\|"bookmark_count":[0-9]*\|"quote_count":[0-9]*\|"retweet_count":[0-9]*' \
    | tr '\n' ' ' >> "$LOG"
  echo " | 12h FINAL" >> "$LOG"
  hermes -p robot-man cron remove ucp-post-watch-30m >/dev/null 2>&1
  exit 0
fi

# Метрики
M=$(xurl --app my-app --auth oauth2 -u RobotsTJ500 "/2/tweets/$POST_ID?tweet.fields=public_metrics" 2>/dev/null \
  | grep -o '"impression_count":[0-9]*\|"like_count":[0-9]*\|"reply_count":[0-9]*\|"bookmark_count":[0-9]*\|"quote_count":[0-9]*\|"retweet_count":[0-9]*' \
  | tr '\n' ' ')
NEWREPLIES=$(xurl --app my-app --auth oauth2 "/2/tweets/search/recent?query=conversation_id%3A$POST_ID%20-is%3Aretweet&max_results=20" 2>/dev/null | grep -c '"id"')
PREV=$(tail -1 "$LOG" 2>/dev/null)
LINE="$NOW | $M | thread_posts:$NEWREPLIES"
echo "$LINE" >> "$LOG"

# Уведомлять только при изменении
if [ -n "$PREV" ] && [ "$PREV" != "$LINE" ]; then
  echo "$LINE"
else
  echo "$NOW | no change"
fi
