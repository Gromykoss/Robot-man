#!/usr/bin/env python3
"""
Robot-man Self-Improvement Analytics Loop.
Runs daily at 15:00 UTC. For posts from yesterday, fetches metrics,
compares with averages, extracts patterns, and triggers voice-updater.

Usage:
  python3 analytics_loop.py                    # Normal run (yesterday's posts)
  python3 analytics_loop.py --days 7           # Last 7 days
  python3 analytics_loop.py --output-dir .     # Write metrics to this dir
  python3 analytics_loop.py --verbose          # Verbose output
"""
import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOME = os.environ.get('HOME', '/home/hermes-workspace')
ROOT = Path(__file__).resolve().parent.parent  # project root (scripts/../)
PUBLISHED_LOG = ROOT / "published_posts.jsonl"
METRICS_DIR = ROOT / "data" / "metrics"
VOICE_UPDATE_DIR = ROOT / "data" / "voice_updates"
ACCOUNT_ID = '1871454196295479296'  # @RobotsTJ500

os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(VOICE_UPDATE_DIR, exist_ok=True)


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


def load_published_posts(days_back=1):
    """Load post IDs from the local log, filter by age."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days_back)
    posts = []
    if not PUBLISHED_LOG.exists():
        print(f"[SKIP] No published_posts.jsonl at {PUBLISHED_LOG}")
        return posts
    with open(PUBLISHED_LOG) as f:
        for line in f:
            try:
                rec = json.loads(line.strip())
                created = datetime.fromisoformat(
                    rec['created_at'].replace('Z', '+00:00')
                )
                age_h = (now - created).total_seconds() / 3600
                # Include posts that are at least 6h old (enough for initial metrics)
                # but within the days_back window
                if created >= cutoff and age_h >= 6:
                    posts.append({'id': rec['id'], 'created_at': created})
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    return posts


def fetch_post_metrics(post_id, retries=2):
    """Fetch full metrics for a single post via X API."""
    url = f'/2/tweets/{post_id}?tweet.fields=public_metrics,created_at,note_tweet,attachments'
    for attempt in range(retries):
        data = xurl([url])
        if data and 'data' in data:
            t = data['data']
            metrics = t.get('public_metrics', {})
            return {
                'id': post_id,
                'created_at': t.get('created_at', ''),
                'likes': metrics.get('like_count', 0),
                'replies': metrics.get('reply_count', 0),
                'retweets': metrics.get('retweet_count', 0),
                'quotes': metrics.get('quote_count', 0),
                'bookmarks': metrics.get('bookmark_count', 0),
                'impressions': metrics.get('impression_count', 0),
                'fetched_at': datetime.now(timezone.utc).isoformat(),
            }
    return None


def load_historical_metrics():
    """Load all historical metrics from metric files for baseline comparison."""
    all_metrics = []
    if METRICS_DIR.exists():
        for f in sorted(METRICS_DIR.glob('metrics_*.json')):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                    if isinstance(data, list):
                        all_metrics.extend(data)
                    elif isinstance(data, dict):
                        all_metrics.append(data)
            except (json.JSONDecodeError, KeyError):
                continue
    # Also check the daily metrics files
    for f in sorted(METRICS_DIR.glob('daily_*.json')):
        try:
            with open(f) as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    all_metrics.extend(data)
        except (json.JSONDecodeError, KeyError):
            continue
    return all_metrics


def compute_averages(metrics):
    """Compute average metrics for baseline comparison."""
    if not metrics:
        return {}
    totals = defaultdict(float)
    count = len(metrics)
    for m in metrics:
        totals['likes'] += m.get('likes', 0)
        totals['replies'] += m.get('replies', 0)
        totals['retweets'] += m.get('retweets', 0)
        totals['bookmarks'] += m.get('bookmarks', 0)
        totals['impressions'] += m.get('impressions', 0)
    return {k: round(v / count, 1) for k, v in totals.items()}


def classify_performance(post, averages):
    """Classify a post relative to baseline."""
    eng = post['likes'] + post['replies'] + post['retweets'] + post['bookmarks']
    avg_eng = averages.get('likes', 1) + averages.get('replies', 0) + \
              averages.get('retweets', 0) + averages.get('bookmarks', 0)

    if avg_eng == 0:
        return 'unknown', 0.0

    ratio = eng / max(avg_eng, 0.1)
    if ratio >= 2.0:
        return 'outperformer', ratio
    elif ratio >= 1.0:
        return 'average', ratio
    else:
        return 'underperformer', ratio


def detect_patterns(metrics, averages):
    """Extract patterns from post performance data."""
    patterns = {'hooks': [], 'formats': [], 'topics': [], 'recommendations': []}

    if not metrics or not averages:
        return patterns

    # Sort by engagement
    sorted_metrics = sorted(
        metrics,
        key=lambda m: m.get('likes', 0) + m.get('replies', 0) + m.get('retweets', 0),
        reverse=True
    )

    best = sorted_metrics[:3] if len(sorted_metrics) >= 3 else sorted_metrics
    worst = sorted_metrics[-3:] if len(sorted_metrics) >= 3 else sorted_metrics

    if best:
        patterns['recommendations'].append(
            f"Best post ({best[0]['id'][:8]}): {best[0].get('likes', 0)} likes, "
            f"{best[0].get('replies', 0)} replies — analyze hook and format"
        )

    if worst and worst[0].get('likes', 1) > 0:
        # Only report if it's a real underperformer, not a new post with 0 likes
        avg_likes = averages.get('likes', 1)
        if worst[0].get('likes', 0) < avg_likes * 0.5:
            patterns['recommendations'].append(
                f"Underperformer ({worst[0]['id'][:8]}): only {worst[0].get('likes', 0)} likes "
                f"vs avg {avg_likes} — avoid similar format/hook"
            )

    # Format pattern detection (based on hook/engagement ratio)
    total_eng = sum(m.get('likes', 0) + m.get('replies', 0) + m.get('retweets', 0) for m in metrics)
    imp = sum(m.get('impressions', 0) for m in metrics)
    if imp > 0:
        eng_rate = total_eng / imp * 100
        patterns['recommendations'].append(
            f"Overall engagement rate: {eng_rate:.1f}% "
            f"({'good' if eng_rate > 5 else 'average' if eng_rate > 2 else 'low'})"
        )

    return patterns


def save_voice_suggestion(patterns, post_id, performance_class, report):
    """Save an observation file for the voice-updater skill to consume."""
    now = datetime.now(timezone.utc)
    filename = f"voice_update_{now.strftime('%Y%m%d')}.json"
    update_path = VOICE_UPDATE_DIR / filename

    suggestion = {
        'date': now.isoformat(),
        'source_run': 'analytics_loop',
        'source_post': post_id,
        'performance': performance_class,
        'patterns': patterns,
        'summary': report.split('\n')[0] if report else 'No significant patterns',
    }

    # Append to a rolling file
    existing = []
    if update_path.exists():
        try:
            with open(update_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, ValueError):
            existing = []

    existing.append(suggestion)
    with open(update_path, 'w') as f:
        json.dump(existing, f, indent=2)

    return update_path


def main():
    parser = argparse.ArgumentParser(description='Robot-man Self-Improvement Analytics Loop')
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to analyze (default: 1)')
    parser.add_argument('--output-dir', type=str, default=str(METRICS_DIR),
                        help='Output directory for metrics files')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    args = parser.parse_args()

    days_back = args.days
    now = datetime.now(timezone.utc)

    print(f"=== Robot-man Self-Improvement Loop === {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Analyzing posts from last {days_back} day(s)\n")

    # 1. Load posts from log
    posts = load_published_posts(days_back)
    if not posts:
        print("[SKIP] No posts found in the analysis window")
        return

    print(f"Found {len(posts)} post(s) to analyze\n")

    # 2. Fetch fresh metrics for each post
    metrics = []
    for p in posts:
        m = fetch_post_metrics(p['id'])
        if m:
            metrics.append(m)
            print(f"  📊 {p['id'][:8]} | ❤️{m['likes']} 💬{m['replies']} "
                  f"🔄{m['retweets']} 🔖{m['bookmarks']} 👁️{m['impressions']}")
        else:
            print(f"  ❌ {p['id'][:8]} | Failed to fetch metrics")
        if args.verbose:
            print(f"     Created at: {p['created_at']}")

    # 3. Load historical baseline
    historical = load_historical_metrics()
    all_metrics = historical + metrics
    averages = compute_averages(all_metrics)

    print(f"\n📈 Baseline (from {len(historical)} historical records):")
    print(f"   Avg likes: {averages.get('likes', 'N/A')}")
    print(f"   Avg replies: {averages.get('replies', 'N/A')}")
    print(f"   Avg retweets: {averages.get('retweets', 'N/A')}")
    print(f"   Avg bookmarks: {averages.get('bookmarks', 'N/A')}")
    print(f"   Avg impressions: {averages.get('impressions', 'N/A')}")

    # 4. Classify each post
    print(f"\n🔍 Performance classification:")
    for m in metrics:
        perf_class, ratio = classify_performance(m, averages)
        eng = m['likes'] + m['replies'] + m['retweets'] + m['bookmarks']
        label = {
            'outperformer': '🏆 OUTPERFORMER',
            'average': '📊 AVERAGE',
            'underperformer': '⚠️ UNDERPERFORMER',
            'unknown': '❓ UNKNOWN',
        }.get(perf_class, 'UNKNOWN')
        print(f"   {label} | {m['id'][:8]} | eng={eng} | ratio={ratio:.1f}x")

    # 5. Detect patterns
    patterns = detect_patterns(metrics, averages)

    # 6. Save daily metrics
    daily_file = METRICS_DIR / f"daily_{now.strftime('%Y%m%d')}.json"
    with open(daily_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n💾 Saved daily metrics to {daily_file.name}")

    # 7. Generate report
    report_lines = []
    report_lines.append(f"Robot-man Analytics — {now.strftime('%Y-%m-%d')}")
    report_lines.append(f"Posts analyzed: {len(metrics)}")
    report_lines.append(f"Total baseline records: {len(all_metrics)}")
    report_lines.append("")

    if metrics:
        best = max(metrics, key=lambda m: m['likes'] + m['replies'] + m['retweets'])
        worst = min(metrics, key=lambda m: m['likes'] + m['replies'] + m['retweets'])
        report_lines.append(f"🏆 Best: {best['id'][:8]} ({best['likes']}❤️ {best['replies']}💬 {best['retweets']}🔄)")
        report_lines.append(f"⚠️ Worst: {worst['id'][:8]} ({worst['likes']}❤️ {worst['replies']}💬 {worst['retweets']}🔄)")

    report_lines.append("")
    report_lines.append("--- Patterns ---")
    for rec in patterns.get('recommendations', []):
        report_lines.append(f"• {rec}")

    report = '\n'.join(report_lines)
    print(f"\n📋 Report:\n{report}")

    # 8. Save voice-updater trigger (for the best post)
    if metrics:
        best_post = max(metrics, key=lambda m: m['likes'] + m['replies'] + m['retweets'])
        perf_class, _ = classify_performance(best_post, averages)
        update_file = save_voice_suggestion(
            patterns, best_post['id'], perf_class, report
        )
        print(f"\n🎙️ Voice-update suggestion saved to {update_file}")

    print("\n✅ Analytics loop complete")


if __name__ == '__main__':
    main()
