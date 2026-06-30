#!/usr/bin/env python3
"""Robot-man analytics: follower count, post metrics, weekly report."""
import subprocess, json, sys, os
from datetime import datetime, timezone

HOME = os.environ.get('HOME', '/home/hermes-workspace')
XD = {'HOME': HOME, 'PATH': os.environ.get('PATH', '')}

def xurl(cmd):
    """Run xurl command, return parsed JSON."""
    result = subprocess.run(
        ['xurl'] + cmd,
        capture_output=True, text=True,
        timeout=20, env=XD
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

def get_followers():
    """Get current follower count."""
    me = xurl(['whoami'])
    if not me or 'data' not in me:
        return None
    uid = me['data']['id']
    username = me['data']['username']
    # Get user with public_metrics via raw API
    user = xurl([f'/2/users/{uid}?user.fields=public_metrics'])
    if not user or 'data' not in user:
        return None
    return {
        'id': uid,
        'username': username,
        'followers': user['data']['public_metrics']['followers_count'],
        'following': user['data']['public_metrics']['following_count'],
        'tweets': user['data']['public_metrics']['tweet_count'],
    }

def get_recent_posts(n=10):
    """Get recent posts with metrics."""
    timeline = xurl(['timeline', '-n', str(n)])
    if not timeline or 'data' not in timeline:
        return []
    
    posts = []
    for t in timeline['data']:
        metrics = t.get('public_metrics', {})
        posts.append({
            'id': t['id'],
            'text': t['text'][:100],
            'created_at': t.get('created_at', ''),
            'likes': metrics.get('like_count', 0),
            'reposts': metrics.get('repost_count', 0),
            'replies': metrics.get('reply_count', 0),
            'impressions': metrics.get('impression_count', 0),
        })
    return posts

def get_replies_to_our_posts():
    """Get mentions/notifications."""
    mentions = xurl(['mentions', '-n', '20'])
    if not mentions or 'data' not in mentions:
        return []
    return mentions['data']

def main():
    print(f"=== Robot-man Analytics === {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    
    # 1. Profile
    followers = get_followers()
    if followers:
        print(f"📊 @{followers['username']}")
        print(f"   Followers: {followers['followers']} (+? since last week)")
        print(f"   Following: {followers['following']}")
        print(f"   Tweets: {followers['tweets']}")
    else:
        print("❌ Could not fetch profile")
    
    print()
    
    # 2. Recent posts
    posts = get_recent_posts(10)
    if posts:
        print("📝 Recent posts:")
        for p in posts[:5]:
            eng = p['likes'] + p['reposts'] + p['replies']
            print(f"   [{p['created_at'][:10]}] ❤️{p['likes']} 🔄{p['reposts']} 💬{p['replies']} 👁️{p['impressions']}")
            print(f"   {p['text'][:90]}...")
        best = max(posts, key=lambda x: x['likes'] + x['reposts'])
        print(f"\n   🏆 Best: ❤️{best['likes']} 🔄{best['reposts']} — {best['text'][:80]}...")
    else:
        print("❌ Could not fetch posts")
    
    print()
    
    # 3. Mentions
    mentions = get_replies_to_our_posts()
    unanswered = [m for m in mentions if m.get('in_reply_to_user_id') == followers['id']] if followers else []
    if unanswered:
        print(f"💬 Unanswered replies: {len(unanswered)}")
    
    print("\n---")

if __name__ == '__main__':
    main()
