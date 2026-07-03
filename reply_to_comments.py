#!/usr/bin/env python3
"""
Comment Reply Engine — отвечает на комментарии к постам @RobotsTJ500.

Правило: ответить на КАЖДЫЙ комментарий в течение 2 часов.
Запуск: каждые 30 минут через cron.
"""
import subprocess, json, sys, os
from datetime import datetime, timezone, timedelta

HOME = os.environ.get('HOME', '/home/hermes-workspace')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'reply_log')
os.makedirs(LOG_DIR, exist_ok=True)

ACCOUNT_ID = '1871454196295479296'  # @RobotsTJ500
MAX_POSTS = 5
REPLY_WINDOW_HOURS = 2
MAX_REPLIES_PER_RUN = 3  # Safety cap


def xurl(cmd):
    """Run xurl, return parsed JSON."""
    result = subprocess.run(
        ['xurl', '--app', 'my-app', '--auth', 'oauth1', '-u', 'RobotsTJ500'] + cmd,
        capture_output=True, text=True, timeout=30,
        env={**os.environ, 'HOME': HOME}
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


PUBLISHED_LOG = os.path.join(os.path.dirname(__file__), 'published_posts.jsonl')


def save_published_post(post_id, created_at=None):
    """Save a post ID after publishing. Called by the posting flow."""
    if created_at is None:
        created_at = datetime.now(timezone.utc).isoformat()
    with open(PUBLISHED_LOG, 'a') as f:
        f.write(json.dumps({'id': str(post_id), 'created_at': created_at}) + '\n')


def get_my_recent_posts():
    """
    Get recent post IDs from local log (survives API outages).
    Falls back to X API only if log is empty or stale.
    """
    now = datetime.now(timezone.utc)
    posts = []

    # 1. Try local log first (fast, survives 503)
    if os.path.exists(PUBLISHED_LOG):
        with open(PUBLISHED_LOG) as f:
            for line in f:
                try:
                    rec = json.loads(line.strip())
                    created = datetime.fromisoformat(rec['created_at'].replace('Z', '+00:00'))
                    age_h = (now - created).total_seconds() / 3600
                    if age_h <= 48:  # Only check posts from last 48h
                        posts.append({'id': rec['id'], 'created_at': rec['created_at']})
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

    if posts:
        return sorted(posts, key=lambda p: p['created_at'], reverse=True)[:MAX_POSTS]

    # 2. Fallback: X API (may be 503)
    data = xurl([
        '/2/users/{}/tweets'.format(ACCOUNT_ID),
        '?max_results={}'.format(MAX_POSTS),
        '&tweet.fields=created_at,conversation_id,public_metrics',
        '&exclude=retweets,replies'
    ])
    if not data or 'data' not in data:
        return []
    return data['data']


def get_comments(conversation_id, since_time=None):
    """Get comments on a post (conversation)."""
    params = [
        '/2/tweets/search/recent',
        '?query=conversation_id:{}'.format(conversation_id),
        '&tweet.fields=created_at,author_id,conversation_id,in_reply_to_user_id',
        '&expansions=author_id',
        '&user.fields=username',
        '&max_results=20'
    ]
    if since_time:
        params[1] += '&start_time=' + since_time
    
    data = xurl(params)
    if not data or 'data' not in data:
        return []
    
    users = {u['id']: u['username'] for u in data.get('includes', {}).get('users', [])}
    comments = []
    for t in data['data']:
        author = users.get(t.get('author_id'), 'unknown')
        # Skip own replies
        if author.lower() == 'robotstj500':
            continue
        comments.append({
            'id': t['id'],
            'author': author,
            'author_id': t.get('author_id'),
            'text': t['text'],
            'created_at': t.get('created_at'),
        })
    return comments


def get_replied_ids():
    """Load set of already-replied comment IDs."""
    log_file = os.path.join(LOG_DIR, 'replied.json')
    if os.path.exists(log_file):
        with open(log_file) as f:
            return set(json.load(f))
    return set()


def save_replied(comment_id, post_id, author, reply_text):
    """Log a reply."""
    replied = get_replied_ids()
    replied.add(comment_id)
    with open(os.path.join(LOG_DIR, 'replied.json'), 'w') as f:
        json.dump(list(replied), f)
    with open(os.path.join(LOG_DIR, 'replies.log'), 'a') as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | post={post_id} | reply_to=@{author} | comment_id={comment_id}\n")


def compose_reply(comment_text, author):
    """Compose a short, useful reply. Caller can override with LLM later."""
    # Simple heuristic: acknowledge + add value
    if '?' in comment_text:
        return f"Good question. Let me break it down in a thread — will post follow-up shortly. 🤖"
    elif len(comment_text) < 50:
        return f"Thanks! More details in the full write-up. Building in public. 🤖"
    else:
        return f"Appreciate the thoughtful take. This is exactly the kind of signal we track. 🤖"


def send_reply(comment_id, text):
    """Reply to a comment. Returns True on success."""
    result = xurl(['reply', comment_id, text])
    if result and 'data' in result:
        return True
    return False


def main():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=REPLY_WINDOW_HOURS)
    replied_ids = get_replied_ids()
    
    posts = get_my_recent_posts()
    if not posts:
        print("[SKIP] No recent posts found")
        return
    
    total_replied = 0
    total_found = 0
    
    for post in posts:
        pid = post['id']
        created = datetime.fromisoformat(post['created_at'].replace('Z', '+00:00'))
        
        # Only check posts from last 24h
        if (now - created).total_seconds() > 86400:
            continue
        
        comments = get_comments(pid, since_time=cutoff.isoformat())
        unreplied = [c for c in comments if c['id'] not in replied_ids]
        total_found += len(unreplied)
        
        for c in unreplied[:MAX_REPLIES_PER_RUN]:
            if total_replied >= MAX_REPLIES_PER_RUN:
                break
            
            reply_text = compose_reply(c['text'], c['author'])
            ok = send_reply(c['id'], reply_text)
            if ok:
                save_replied(c['id'], pid, c['author'], reply_text)
                total_replied += 1
                print(f"✅ Replied to @{c['author']} on post {pid[:8]}")
            else:
                print(f"❌ Failed reply to @{c['author']} on post {pid[:8]}")
    
    print(f"\nSummary: {total_replied} replies sent, {total_found} comments found")
    if total_found == 0:
        print("[OK] No unreplied comments in 2h window")


if __name__ == '__main__':
    main()
