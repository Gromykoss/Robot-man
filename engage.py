#!/usr/bin/env python3
"""
Robot-man engagement engine.
Finds relevant posts → filters → presents candidates for Hermes to act on.

Safety: read-only by default. Hermes decides which actions to take.
"""
import subprocess, json, sys, os
from datetime import datetime, timezone, timedelta

HOME = os.environ.get('HOME', '/home/hermes-workspace')
XD = {'HOME': HOME, 'PATH': os.environ.get('PATH', '')}
LOG_DIR = os.path.join(os.path.dirname(__file__), 'engagement_log')
os.makedirs(LOG_DIR, exist_ok=True)

# === CONFIG ===
SEARCH_TOPICS = [
    'Hermes Agent agent workflow',
    'HermesAgent skill memory',
    'building AI agent infrastructure',
    'Hermes Agent Claude Code Codex',
    'AI memory agent production',
    'self improving AI context',
    '@NousResearch Hermes deployment',
    'agent-driven development',
]

SKIP_HANDLES = {'RobotsTJ500', 'Gromykoss', 'gromykoss'}
MAX_CANDIDATES = 10
MAX_AGE_HOURS = 24

# Quality thresholds
MIN_LIKES = 1            # skip zero-engagement posts (bots/spam)
MAX_LIKES = 500          # skip viral (we can't add value)
MIN_TEXT_LENGTH = 60     # skip one-liners, emoji-only
MIN_REPLIES = 0          # allow any reply count
MAX_REPLIES = 100        # skip flooded threads

# Interesting signal words (posts with these get priority)
SIGNAL_WORDS = [
    'build', 'built', 'building',
    'workflow', 'pipeline', 'automate',
    'memory', 'context', 'skill',
    'infrastructure', 'deploy', 'production',
    'question', 'how', 'anyone',
    'tried', 'testing', 'experiment',
    'learned', 'lesson', 'insight',
    'open source', 'repo', 'github',
]

# === TOOL WRAPPERS ===

def xurl(cmd):
    """Run xurl, return parsed JSON."""
    result = subprocess.run(
        ['xurl'] + cmd,
        capture_output=True, text=True, timeout=25, env=XD
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def search_topic(query, n=10):
    """Search for recent posts on a topic."""
    data = xurl(['search', query, '-n', str(n), '--app', 'my-app'])
    if not data or 'data' not in data:
        return []
    users = {u['id']: u['username'] for u in data.get('includes', {}).get('users', [])}
    results = []
    for t in data['data']:
        author = users.get(t.get('author_id'), 'unknown')
        if author.lower() in SKIP_HANDLES:
            continue
        results.append({
            'id': t['id'],
            'author': author,
            'text': t['text'],
            'created_at': t.get('created_at', ''),
            'metrics': t.get('public_metrics', {}),
        })
    return results


def get_engaged_ids():
    """Read log of already-engaged post IDs."""
    log_file = os.path.join(LOG_DIR, 'engaged.json')
    if os.path.exists(log_file):
        with open(log_file) as f:
            return set(json.load(f))
    return set()


def save_engaged(post_id, action):
    """Log an engagement action."""
    engaged = get_engaged_ids()
    engaged.add(post_id)
    with open(os.path.join(LOG_DIR, 'engaged.json'), 'w') as f:
        json.dump(list(engaged), f)
    # Also log the action
    with open(os.path.join(LOG_DIR, 'actions.log'), 'a') as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | {action} | {post_id}\n")


def filter_candidates(posts, engaged_ids):
    """Filter: skip already engaged, too old, self-posts."""
    now = datetime.now(timezone.utc)
    good = []
    for p in posts:
        pid = p['id']
        if pid in engaged_ids:
            continue
        # Age check
        try:
            created = datetime.fromisoformat(p['created_at'].replace('Z', '+00:00'))
            age = (now - created).total_seconds() / 3600
            if age > MAX_AGE_HOURS:
                continue
        except (ValueError, TypeError):
            pass
        good.append(p)
    return good[:MAX_CANDIDATES]


# === MAIN ===

def find_engagement_targets():
    """Find posts worth engaging with. Returns list of candidates."""
    engaged_ids = get_engaged_ids()
    all_candidates = []

    for topic in SEARCH_TOPICS:
        try:
            posts = search_topic(topic, n=5)
        except Exception:
            continue
        if not posts:
            continue
        for p in posts:
            likes = p['metrics'].get('like_count', 0)
            replies = p['metrics'].get('reply_count', 0)
            text = p['text']
            
            # Quality gates
            if likes < MIN_LIKES or likes > MAX_LIKES:
                continue
            if replies > MAX_REPLIES:
                continue
            if len(text) < MIN_TEXT_LENGTH:
                continue
            # Skip retweets (start with "RT @")
            if text.strip().startswith('RT @'):
                continue
            # Score: signal words × 2 + likes
            text_lower = text.lower()
            signal_score = sum(2 for w in SIGNAL_WORDS if w in text_lower)
            p['_quality'] = signal_score + min(likes, 50)  # cap likes weight
            all_candidates.append(p)

    # Deduplicate by ID
    seen = set()
    unique = []
    for p in all_candidates:
        if p['id'] not in seen:
            seen.add(p['id'])
            unique.append(p)

    candidates = filter_candidates(unique, engaged_ids)

    # Sort by quality score descending
    candidates.sort(key=lambda x: x.get('_quality', 0), reverse=True)

    return candidates


def print_candidates(candidates):
    """Pretty-print engagement candidates."""
    if not candidates:
        print("No engagement candidates found.")
        return

    print(f"=== Engagement Candidates ({len(candidates)}) ===\n")
    for i, p in enumerate(candidates[:5], 1):
        likes = p['metrics'].get('like_count', 0)
        replies = p['metrics'].get('reply_count', 0)
        text = p['text'].replace('\n', ' ')[:120]
        print(f"{i}. @{p['author']} | ❤️{likes} 💬{replies}")
        print(f"   {text}...")
        print(f"   id: {p['id']}")
        print()


def do_like(post_id):
    """Like a post. Returns True on success."""
    result = xurl(['like', post_id, '--app', 'my-app'])
    if result and 'data' in result:
        save_engaged(post_id, 'like')
        return True
    return False


def do_reply(post_id, text):
    """Reply to a post. Returns True on success."""
    result = xurl(['reply', post_id, text, '--app', 'my-app'])
    if result and 'data' in result:
        save_engaged(post_id, 'reply')
        return True
    return False


def do_follow(username):
    """Follow a user."""
    result = xurl(['follow', f'@{username}', '--app', 'my-app'])
    return result and 'data' in result


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--act':
        # Action mode: like/reply based on stdin
        action = json.load(sys.stdin)
        aid = action.get('id')
        act = action.get('action')
        if act == 'like' and aid:
            ok = do_like(aid)
            print(f"{'✅' if ok else '❌'} liked {aid}")
        elif act == 'reply' and aid:
            text = action.get('text', '')
            ok = do_reply(aid, text)
            print(f"{'✅' if ok else '❌'} replied to {aid}")
        elif act == 'follow':
            user = action.get('user', '')
            ok = do_follow(user)
            print(f"{'✅' if ok else '❌'} followed @{user}")
    else:
        # Discovery mode: find and print candidates
        candidates = find_engagement_targets()
        print_candidates(candidates)
        # Output JSON for programmatic use
        if '--json' in sys.argv:
            print(json.dumps(candidates[:5], indent=2, default=str))
