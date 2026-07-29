#!/usr/bin/env python3
"""
Robot-man engagement engine.
Finds relevant posts → filters → ranks with xcurate-inspired scoring → presents candidates.

Scoring formula:
  score = recency_factor(age_h) × normalized_author_weight × raw_engagement × (1 − penalty) × bucket_multiplier

Scores combine 5 signals from xcurate's rank.ts:
  1. Exponential recency decay  —  fresh ~1.0, 24h-old ~0.05
  2. Replies weight double       —  raw_engagement = likes + 2×replies + quotes
  3. Content quality penalties   —  walls of text, emoji-only, hashtag spam
  4. Ad/link detection           —  drops pure-link and promo/giveaway posts
  5. Composite score formula     —  multiplicative across all factors

Safety: read-only by default. Hermes decides which actions to take.
Use --dry-run to preview without side effects. Use --verbose for debug output.
"""
import subprocess, json, sys, os, math, re
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
WINDOW_HOURS = 24          # hard age cutoff; recency_factor handles scoring within window

# Tracked authors — higher weight = more likely to engage (normalized against max)
TRACKED_AUTHORS = {
    'NousResearch': 2.0,
}
DEFAULT_AUTHOR_WEIGHT = 1.0

# Quality thresholds
MIN_LIKES = 1            # skip zero-engagement posts (bots/spam)
MAX_LIKES = 500          # skip viral (we can't add value)
MIN_TEXT_LENGTH = 60     # skip one-liners, emoji-only
MIN_REPLIES = 0          # allow any reply count
MAX_REPLIES = 100        # skip flooded threads

# Interesting signal words (posts with these get priority via bucket_multiplier)
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


# ======================================================================
#  xcurate-inspired scoring functions (from rank.ts §7)
# ======================================================================

def recency_factor(age_hours, window_hours=24):
    """
    Exponential recency decay (xcurate default).
    Fresh posts get ~1.0; posts at the window boundary get ~0.05.
    """
    return math.exp(-age_hours / (window_hours / 3))


def raw_engagement_value(like_count, reply_count, quote_count):
    """
    Raw engagement signal with replies weighted double.
    Replies signal conversation quality (per xcurate rank.ts:49).
    """
    return like_count + 2 * reply_count + quote_count


def penalty_for(text):
    """
    Content quality penalties. Returns a value in [0, 1]; higher = worse.
    Penalises: walls of text (>600 chars), emoji-only posts, hashtag spam.
    Based on rank.ts:57-66.
    """
    p = 0.0
    if len(text) > 600:
        p += 0.5                    # wall of text
    letters = sum(1 for c in text if c.isalpha())
    emoji_count = sum(1 for c in text if ord(c) >= 0x1F000)  # chars in emoji blocks
    if letters < 5 and emoji_count >= 1:
        p += 0.6                    # basically just emoji
    hashtags = len(re.findall(r'#\w+', text))
    if hashtags >= 3:
        p += 0.4                    # hashtag spam
    return min(p, 1.0)


def is_link_or_ad(text):
    """
    Coarse drop heuristic: a tweet that is essentially just a link, or an ad.
    Based on rank.ts:69-76.
    """
    stripped = re.sub(r'https?://\S+', '', text).strip()
    has_link = bool(re.search(r'https?://', text))
    if has_link and len(stripped) < 12:
        return True
    ad_pattern = (
        r'\b(giveaway|airdrop|promo\s?code|use\s+code|discount\s+code'
        r'|buy\s+now|limited\s+offer|sign\s+up\s+now|link\s+in\s+bio)\b'
    )
    if re.search(ad_pattern, text, re.IGNORECASE):
        return True
    return False


def normalized_author_weight(author_handle):
    """
    Account priority: tracked authors get higher weight (normalized against max).
    Non-tracked authors get DEFAULT_AUTHOR_WEIGHT.
    """
    weight = TRACKED_AUTHORS.get(author_handle, DEFAULT_AUTHOR_WEIGHT)
    max_w = max(TRACKED_AUTHORS.values()) if TRACKED_AUTHORS else DEFAULT_AUTHOR_WEIGHT
    return weight / max(max_w, 1)


def bucket_multiplier_for(text):
    """
    Topic relevance multiplier from SIGNAL_WORDS matching.
    0 matches → 0.5 (low relevance)
    1 match   → 1.0 (baseline)
    2 matches → 1.3
    3+        → 1.5 (high relevance)
    """
    text_lower = text.lower()
    matches = sum(1 for w in SIGNAL_WORDS if w in text_lower)
    if matches == 0:
        return 0.5
    elif matches == 1:
        return 1.0
    elif matches == 2:
        return 1.3
    else:
        return 1.5


# === CANDIDATE DISCOVERY ===

def parse_post_age(created_at_str):
    """Parse a post's created_at into age in hours. Returns None on failure."""
    try:
        created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        age_h = (datetime.now(timezone.utc) - created).total_seconds() / 3600
        return age_h
    except (ValueError, TypeError):
        return None


def filter_candidates(posts, engaged_ids):
    """Deduplicate, skip already-engaged, and enforce hard age cutoff."""
    now = datetime.now(timezone.utc)
    good = []
    seen_ids = set()
    for p in posts:
        pid = p['id']
        if pid in engaged_ids or pid in seen_ids:
            continue
        seen_ids.add(pid)
        # Hard age cutoff (recency_factor handles scoring within window)
        try:
            created = datetime.fromisoformat(p['created_at'].replace('Z', '+00:00'))
            age = (now - created).total_seconds() / 3600
            if age > WINDOW_HOURS:
                continue
        except (ValueError, TypeError):
            pass
        good.append(p)
    return good[:MAX_CANDIDATES]


def find_engagement_targets(verbose=False):
    """
    Find posts worth engaging with. Returns list of candidates ranked by
    the xcurate-inspired composite score.
    """
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
            quotes = p['metrics'].get('quote_count', 0)
            text = p['text']
            author = p['author']

            # --- Quality gates (same as before) ---
            if likes < MIN_LIKES or likes > MAX_LIKES:
                continue
            if replies > MAX_REPLIES:
                continue
            if len(text) < MIN_TEXT_LENGTH:
                continue
            if text.strip().startswith('RT @'):
                continue

            # --- xcurate-inspired drops ---
            if is_link_or_ad(text):
                if verbose:
                    print(f"  DROP @{author}: link/ad detected")
                continue

            # --- Parse age ---
            age_h = parse_post_age(p['created_at'])
            if age_h is None or age_h > WINDOW_HOURS:
                continue

            # --- Compute scoring factors ---
            rf = recency_factor(age_h, WINDOW_HOURS)
            nw = normalized_author_weight(author)
            re_val = raw_engagement_value(likes, replies, quotes)
            pnlty = penalty_for(text)
            bm = bucket_multiplier_for(text)

            # Composite score (multiplicative, per xcurate)
            score = rf * nw * re_val * (1.0 - pnlty) * bm

            # Store factors on the candidate dict for downstream use
            p['_score'] = round(score, 4)
            p['_age_h'] = round(age_h, 1)
            p['_recency'] = round(rf, 3)
            p['_engagement'] = int(re_val)
            p['_penalty'] = round(pnlty, 2)
            p['_bucket_mult'] = round(bm, 1)
            p['_author_weight'] = round(nw, 1)

            if verbose:
                print(
                    f"  @{author:<20} rf={rf:.3f} nw={nw:.1f} "
                    f"eng={int(re_val):<4} pen={pnlty:.2f} bm={bm:.1f} "
                    f"→ {score:.3f} | age={age_h:.1f}h | {text[:60].replace(chr(10), ' ')}..."
                )

            all_candidates.append(p)

    candidates = filter_candidates(all_candidates, engaged_ids)

    # Sort by composite score descending
    candidates.sort(key=lambda x: x.get('_score', 0), reverse=True)

    return candidates


def print_candidates(candidates, verbose=False):
    """Pretty-print engagement candidates."""
    if not candidates:
        print("No engagement candidates found.")
        return

    print(f"=== Engagement Candidates ({len(candidates)}) ===\n")
    for i, p in enumerate(candidates[:5], 1):
        likes = p['metrics'].get('like_count', 0)
        replies = p['metrics'].get('reply_count', 0)
        quotes = p['metrics'].get('quote_count', 0)
        text = p['text'].replace('\n', ' ')[:120]
        score = p.get('_score', 0)

        print(f"{i}. @{p['author']} | ❤️{likes} 💬{replies} 🔄{quotes} | score={score:.3f}")
        print(f"   {text}...")
        if verbose:
            age = p.get('_age_h', '?')
            rf = p.get('_recency', '?')
            pen = p.get('_penalty', '?')
            bm = p.get('_bucket_mult', '?')
            nw = p.get('_author_weight', '?')
            eng = p.get('_engagement', '?')
            print(f"   age={age}h rf={rf} nw={nw} eng={eng} pen={pen} bm={bm}")
        print(f"   id: {p['id']}")
        print()


# === ACTIONS ===

def do_like(post_id, dry_run=False):
    """Like a post. Returns True on success."""
    if dry_run:
        print(f"  [DRY RUN] would like {post_id}")
        return True
    result = xurl(['like', post_id, '--app', 'my-app'])
    if result and 'data' in result:
        save_engaged(post_id, 'like')
        return True
    return False


def do_reply(post_id, text, dry_run=False):
    """Reply to a post. Returns True on success."""
    if dry_run:
        print(f"  [DRY RUN] would reply to {post_id}: {text[:80]}...")
        return True
    result = xurl(['reply', post_id, text, '--app', 'my-app'])
    if result and 'data' in result:
        save_engaged(post_id, 'reply')
        return True
    return False


def do_follow(username, dry_run=False):
    """Follow a user."""
    if dry_run:
        print(f"  [DRY RUN] would follow @{username}")
        return True
    result = xurl(['follow', f'@{username}', '--app', 'my-app'])
    return result and 'data' in result


# === MAIN ===

def _usage():
    print("Usage: python3 engage.py [--help] [--verbose] [--dry-run] [--json] [--act]")
    print()
    print("Discovery mode (default):  find and print engagement candidates.")
    print("  --json       extra JSON output for programmatic use")
    print("  --verbose    show per-candidate debug scoring details")
    print("  --dry-run    no-op mode (discovery is already read-only, but explicit)")
    print()
    print("Action mode:               like/reply/follow via stdin JSON.")
    print("  --act        read JSON action from stdin")
    print("  --dry-run    simulate action without writing to X")
    print()
    print("Example:")
    print("  python3 engage.py --verbose")
    print("  echo '{\"id\":\"123\",\"action\":\"like\"}' | python3 engage.py --act")
    print("  echo '{\"id\":\"123\",\"action\":\"reply\",\"text\":\"nice!\"}' | python3 engage.py --act --dry-run")


if __name__ == '__main__':
    args = sys.argv[1:]
    verbose = '--verbose' in args
    dry_run = '--dry-run' in args
    show_json = '--json' in args

    if '--help' in args or '-h' in args:
        _usage()
        sys.exit(0)

    if '--act' in args:
        # Action mode: like/reply/follow based on stdin
        action = json.load(sys.stdin)
        aid = action.get('id')
        act = action.get('action')

        if dry_run:
            print("[DRY RUN MODE — no real actions will be taken]\n")

        if act == 'like' and aid:
            ok = do_like(aid, dry_run=dry_run)
            print(f"{'✅' if ok else '❌'} liked {aid}")
        elif act == 'reply' and aid:
            text = action.get('text', '')
            ok = do_reply(aid, text, dry_run=dry_run)
            print(f"{'✅' if ok else '❌'} replied to {aid}")
        elif act == 'follow':
            user = action.get('user', '')
            ok = do_follow(user, dry_run=dry_run)
            print(f"{'✅' if ok else '❌'} followed @{user}")
        else:
            print(f"❌ Unknown action: {act}")
            sys.exit(1)
    else:
        # Discovery mode: find and print candidates
        if dry_run:
            print("[DRY RUN MODE — no real actions will be taken]\n")

        candidates = find_engagement_targets(verbose=verbose)
        print_candidates(candidates, verbose=verbose)

        # Output JSON for programmatic use (cron-compatible)
        if show_json:
            print(json.dumps(candidates[:5], indent=2, default=str))
