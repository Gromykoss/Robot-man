#!/bin/bash
# Wrapper: post to X + save ID to published_posts.jsonl for reply engine.
# Usage:
#   post_with_log.sh "post text" [image_path]          — original post
#   post_with_log.sh --reply TARGET_ID "reply text"    — reply (no cover needed)
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$DIR/published_posts.jsonl"

MODE="post"
if [ "$1" = "--reply" ]; then
    MODE="reply"
    shift
fi

TEXT="$1"
IMAGE="$2"
ACCOUNT="${POST_ACCOUNT:-RobotsTJ500}"

if [ -z "$TEXT" ]; then
    echo "Usage: post_with_log.sh 'text' [image.png]"
    echo "       post_with_log.sh --reply TARGET_ID 'text'"
    exit 1
fi

if [ "$MODE" = "reply" ]; then
    # ── REPLY MODE ──────────────────────────────────────────────
    # Replies do not require a cover. Target must be numeric post ID
    # (same validation as xurl-post-guard reply: 15-25 digits).
    REPLY_TARGET="$TEXT"
    REPLY_BODY="${2:-}"

    if ! echo "$REPLY_TARGET" | grep -qE '^[0-9]{15,25}$'; then
        echo "BLOCKED: --reply requires numeric target post ID (15-25 digits)" >&2
        exit 1
    fi
    if [ -z "$REPLY_BODY" ]; then
        echo "Usage: post_with_log.sh --reply TARGET_ID 'text'" >&2
        exit 1
    fi

    # Replies carry no cover — the checklist media gate would hard-block every
    # reply against a brief that names a cover image. Pass the brief's cover
    # path so the gate verifies the brief is intact but doesn't demand media.
    BRIEF_COVER=$(grep -m1 '^| Изображение |' "$DIR/CONTENT_BRIEF.md" 2>/dev/null | awk -F'|' '{print $3}' | xargs)
    if [ -n "$BRIEF_COVER" ] && [ "$BRIEF_COVER" != "нет" ] && [ "$BRIEF_COVER" != "no" ]; then
        export POST_IMAGE="$BRIEF_COVER"
    fi

    # Operator pipeline gate: same write-limit/approval checks as original posts.
    # Reply counts against the daily public-write budget.
    PYTHONPATH="$DIR" python3 -m operators.operator_pipeline "$REPLY_BODY" "$APPROVAL_TOKEN" || { echo "BLOCKED by operator pipeline" >&2; exit 1; }

    TEXT_TMP=$(mktemp /tmp/robotman_reply_text.XXXXXX)
    printf '%s' "$REPLY_BODY" > "$TEXT_TMP"
    OUTPUT=$(sudo -n /usr/local/bin/xurl-post-guard reply --reply-to "$REPLY_TARGET" --text-file "$TEXT_TMP" 2>&1)
    rm -f "$TEXT_TMP"

    echo "$OUTPUT"

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
    f.write(json.dumps({'id': '$POST_ID', 'created_at': datetime.now(timezone.utc).isoformat(), 'type': 'reply', 'target': '$REPLY_TARGET'}) + '\n')
"
        echo "[LOG] Saved reply $POST_ID (target $REPLY_TARGET) to published_posts.jsonl"
        REPLY_URL="https://x.com/RobotsTJ500/status/$POST_ID"
        TIME_NOW=$(date -u +"%Y-%m-%d %H:%M UTC")
        bash ~/.hermes/scripts/discord-post.sh "1525718586059001906" \
            "**🐦 New Reply** — $TIME_NOW
${REPLY_BODY:0:200}
→ $REPLY_URL" 2>/dev/null
    else
        echo "WARNING: reply sent but no post ID extracted — check guard output above" >&2
    fi
    exit 0
fi

# ── ORIGINAL POST MODE ──────────────────────────────────────────
# Pass the cover path into the operator pipeline so the checklist gate can
# verify that a required image is actually present.
export POST_IMAGE="$IMAGE"

PYTHONPATH="$DIR" python3 -m operators.operator_pipeline "$TEXT" "$APPROVAL_TOKEN" || { echo "BLOCKED by operator pipeline" >&2; exit 1; }

# 03.09.2026: @RobotsTJ500 original posts require a cover. Text-only path is a
# hard block (was WARNING → silent text-only publish). Opt-out only via
# ALLOW_TEXT_ONLY=1 for rare non-cover cases Sergey explicitly ordered.
if [ -z "$IMAGE" ]; then
    if [ "${ALLOW_TEXT_ONLY:-0}" = "1" ]; then
        echo "ALLOW_TEXT_ONLY=1 — text-only publish (explicit override)" >&2
    else
        echo "BLOCKED: cover image required. Usage: post_with_log.sh 'text' /path/cover.png" >&2
        echo "Opt-out only with ALLOW_TEXT_ONLY=1 after Sergey explicit order." >&2
        exit 1
    fi
fi

if [ -n "$IMAGE" ]; then
    # If IMAGE is a URL, download it first
    if echo "$IMAGE" | grep -qE '^https?://'; then
        TMP_IMG="/tmp/post_cover_$$.png"
        curl -sL "$IMAGE" -o "$TMP_IMG" || { echo "ERROR: failed to download $IMAGE"; exit 1; }
        IMAGE="$TMP_IMG"
    fi

    if [ -f "$IMAGE" ]; then
        # Post with image — upload via root guard (write OAuth lives only in /root/.xurl)
        UPLOAD_OUT=$(sudo -n /usr/local/bin/xurl-post-guard media-upload --file "$IMAGE" --media-type image/png 2>&1)
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
        TEXT_TMP=$(mktemp /tmp/robotman_post_text.XXXXXX)
        printf '%s' "$TEXT" > "$TEXT_TMP"
        OUTPUT=$(sudo -n /usr/local/bin/xurl-post-guard post --text-file "$TEXT_TMP" --media-id "$MEDIA_ID" 2>&1)
        rm -f "$TEXT_TMP"
    else
        echo "BLOCKED: image file not found: $IMAGE (no text-only fallback)" >&2
        exit 1
    fi
else
    # Text-only only when ALLOW_TEXT_ONLY=1
    TEXT_TMP=$(mktemp /tmp/robotman_post_text.XXXXXX)
    printf '%s' "$TEXT" > "$TEXT_TMP"
    OUTPUT=$(sudo -n /usr/local/bin/xurl-post-guard post --text-file "$TEXT_TMP" 2>&1)
    rm -f "$TEXT_TMP"
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
