#!/bin/bash
# Wrapper: post to X + save ID to published_posts.jsonl for reply engine.
# Usage: post_with_log.sh "post text" [image_path]
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$DIR/published_posts.jsonl"

TEXT="$1"
IMAGE="$2"

if [ -z "$TEXT" ]; then
    echo "Usage: post_with_log.sh 'text' [image.png]"
    exit 1
fi

if [ -n "$IMAGE" ] && [ -f "$IMAGE" ]; then
    # Post with image
    MEDIA_ID=$(xurl --app my-app --auth oauth1 media upload --media-type image/png --category tweet_image "$IMAGE" 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
    OUTPUT=$(xurl --app my-app --auth oauth1 -u RobotsTJ500 post "$TEXT" --media-id "$MEDIA_ID" 2>&1)
else
    # Text-only post
    OUTPUT=$(xurl --app my-app --auth oauth1 -u RobotsTJ500 post "$TEXT" 2>&1)
fi

echo "$OUTPUT"

# Extract post ID and save
POST_ID=$(echo "$OUTPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('data', {}).get('id', ''))
" 2>/dev/null)

if [ -n "$POST_ID" ]; then
    python3 -c "
import json
from datetime import datetime, timezone
with open('$LOG', 'a') as f:
    f.write(json.dumps({'id': '$POST_ID', 'created_at': datetime.now(timezone.utc).isoformat()}) + '\n')
"
    echo "[LOG] Saved post $POST_ID to published_posts.jsonl"
fi
