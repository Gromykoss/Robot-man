#!/bin/bash
# Wrapper: post to X + save ID to published_posts.jsonl for reply engine.
# Usage: post_with_log.sh "post text" [image_path]
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$DIR/published_posts.jsonl"

TEXT="$1"
IMAGE="$2"
ACCOUNT="${POST_ACCOUNT:-RobotsTJ500}"

if [ -z "$TEXT" ]; then
    echo "Usage: post_with_log.sh 'text' [image.png]"
    exit 1
fi

PYTHONPATH="$DIR" python3 -m operators.operator_pipeline "$TEXT" "$APPROVAL_TOKEN" || { echo "BLOCKED by operator pipeline" >&2; exit 1; }

if [ -n "$IMAGE" ]; then
    # If IMAGE is a URL, download it first
    if echo "$IMAGE" | grep -qE '^https?://'; then
        TMP_IMG="/tmp/post_cover_$$.png"
        curl -sL "$IMAGE" -o "$TMP_IMG" || { echo "ERROR: failed to download $IMAGE"; exit 1; }
        IMAGE="$TMP_IMG"
    fi

    if [ -f "$IMAGE" ]; then
        # Post with image — xurl outputs JSON + human-readable line, extract JSON part only
        UPLOAD_OUT=$(xurl --app my-app --auth oauth1 media upload --media-type image/png --category tweet_image "$IMAGE" 2>&1)
        MEDIA_ID=$(echo "$UPLOAD_OUT" | python3 -c "
import sys, json
lines = sys.stdin.read().strip().split('\n')
# Find the first { and last } to extract JSON block
json_start = next(i for i, l in enumerate(lines) if l.strip() == '{')
json_block = '\n'.join(lines[json_start:])
# Parse only up to the first complete JSON object
decoder = json.JSONDecoder()
data, _ = decoder.raw_decode(json_block)
print(data['data']['id'])
")
        OUTPUT=$(xurl --app my-app --auth oauth1 -u "$ACCOUNT" post "$TEXT" --media-id "$MEDIA_ID" 2>&1)
    else
        echo "WARNING: image file not found — posting text-only"
        OUTPUT=$(xurl --app my-app --auth oauth1 -u "$ACCOUNT" post "$TEXT" 2>&1)
    fi
else
    # Text-only post
    OUTPUT=$(xurl --app my-app --auth oauth1 -u "$ACCOUNT" post "$TEXT" 2>&1)
fi

echo "$OUTPUT"

# Extract post ID and save (tolerant: xurl may emit human-readable lines around JSON)
POST_ID=$(echo "$OUTPUT" | python3 -c "
import sys, json, re
raw = sys.stdin.read()
m = re.search(r'\{.*\}', raw, re.DOTALL)
if not m:
    print('')
else:
    try:
        data = json.loads(m.group(0))
        print(data.get('data', {}).get('id', '') or '')
    except json.JSONDecodeError:
        print('')
" 2>/dev/null)

if [ -n "$POST_ID" ]; then
    PYTHONPATH="$DIR" python3 -m operators.operator_pipeline --increment-write

    python3 -c "
import json
from datetime import datetime, timezone
with open('$LOG', 'a') as f:
    f.write(json.dumps({'id': '$POST_ID', 'created_at': datetime.now(timezone.utc).isoformat()}) + '\n')
"
    echo "[LOG] Saved post $POST_ID to published_posts.jsonl"

    # Push to Discord #robot-human via shared helper
    POST_URL="https://x.com/RobotsTJ500/status/$POST_ID"
    TIME_NOW=$(date -u +"%Y-%m-%d %H:%M UTC")
    bash ~/.hermes/scripts/discord-post.sh "1525718586059001906" \
        "**🐦 New Post** — $TIME_NOW
${TEXT:0:200}...
$POST_URL" 2>/dev/null
fi
