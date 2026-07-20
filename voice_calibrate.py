#!/usr/bin/env python3
"""
Voice Calibration Tool — learns @RobotsTJ500 voice from real replies.

Reads data/my-replies.json, buckets replies by age, extracts voice traits
from the freshest bucket, validates against older buckets, and writes:
  - VOICE_PROFILE.proposed.md (proposal, never overwrites VOICE_PROFILE.md)
  - data/voice_calibration_report.md (evidence + drift notes)

Inspired by xcurate's calibrate-voice command.
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from statistics import median as stats_median

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
REPLIES_PATH = PROJECT_DIR / "data" / "my-replies.json"
VOICE_PROFILE = PROJECT_DIR / "VOICE_PROFILE.md"
PROPOSED_PATH = PROJECT_DIR / "VOICE_PROFILE.proposed.md"
REPORT_PATH = PROJECT_DIR / "data" / "voice_calibration_report.md"

NOW = datetime.now(timezone.utc)

# ---------------------------------------------------------------------------
# Emoji detection
# ---------------------------------------------------------------------------

_EMOJI_RE = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map
    "\U0001f700-\U0001f77f"  # alchemical
    "\U0001f780-\U0001f7ff"  # geometric shapes extended
    "\U0001f800-\U0001f8ff"  # supplemental arrows-c
    "\U0001f900-\U0001f9ff"  # supplemental symbols
    "\U0001fa00-\U0001fa6f"  # chess symbols
    "\U0001fa70-\U0001faff"  # symbols extended-a
    "\U0001fb00-\U0001fbff"  # symbols for legacy computing
    "\U00002600-\U000026ff"  # misc symbols
    "\U00002700-\U000027bf"  # dingbats
    "\U00002300-\U000023ff"  # misc technical
    "\U00002b50"             # star
    "\U00002764-\U00002767"  # heart etc
    "\U0001f1e0-\U0001f1ff"  # flags
    "]+", flags=re.UNICODE)

_HASHTAG_RE = re.compile(r"#\w+")

# ---------------------------------------------------------------------------
# Move classification (keyword heuristic)
# ---------------------------------------------------------------------------

ASK_WORDS = {
    "?", "what", "how", "why", "when", "where", "who",
    "can you", "could you", "would you", "do you", "does",
    "anyone", "anybody", "thoughts", "wdyt", "help",
}

AGREE_WORDS = {
    "yes", "yeah", "yep", "agreed", "exactly", "💯",
    "👏", "this", "+1", "+100", "spot on", "nailed",
    "correct", "true", "facts", "well said", "preach",
}

PUSH_BACK_WORDS = {
    "but", "however", "disagree", "not quite", "actually",
    "i don't think", "respectfully", "counter", "counterpoint",
    "i'd argue", "on the other hand", "the problem is",
    "that's not", "that's incorrect", "i see it differently",
}

ASSERT_WORDS = {
    "i built", "we built", "i shipped", "we shipped",
    "i deployed", "we deployed", "i fixed", "we fixed",
    "here's", "this is", "the answer", "the reason",
    "because", "in my experience", "i've found", "my take",
}


def _word_intersection(text_lower: str, word_set: set) -> int:
    """Count how many signal words appear in the text."""
    return sum(1 for w in word_set if w in text_lower)


def classify_move(text: str) -> str:
    """Return one of: ask, assert, agree, push_back, neutral."""
    t = text.strip().lower()
    scores = {
        "ask":       _word_intersection(t, ASK_WORDS),
        "agree":     _word_intersection(t, AGREE_WORDS),
        "push_back": _word_intersection(t, PUSH_BACK_WORDS),
        "assert":    _word_intersection(t, ASSERT_WORDS),
    }
    # boost assert for long declarative text without other strong signals
    if len(text) > 120 and all(v <= 1 for v in scores.values()):
        scores["assert"] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "neutral"


# ---------------------------------------------------------------------------
# Opening / closing pattern extraction
# ---------------------------------------------------------------------------

def extract_opening(text: str) -> str:
    """Extract opening pattern (first ~60 chars or first sentence)."""
    t = text.strip()
    # take first sentence or first 80 chars
    cut = min(len(t), 80)
    for punc in ".!?\n":
        idx = t[:cut].find(punc)
        if idx > 10:
            return t[:idx + 1].strip()
    return t[:cut].strip() + "…"


def extract_closing(text: str) -> str:
    """Extract closing pattern (last sentence or last ~60 chars)."""
    t = text.strip()
    if len(t) <= 80:
        return t
    # Take last sentence
    for punc in ".!?\n":
        idx = t.rfind(punc, max(0, len(t) - 80))
        if idx > len(t) * 0.6:
            return t[idx + 1:].strip()
    return t[-60:].strip()


# ---------------------------------------------------------------------------
# Anti-tell detection (heuristic)
# ---------------------------------------------------------------------------

def detect_anti_tells(replies: list[dict]) -> list[str]:
    """Detect patterns NEVER observed across the corpus."""
    anti_tells = []
    has_all_caps = any(
        re.search(r"\b[A-Z]{2,}\b", r["text"]) and
        not any(w in r["text"].lower() for w in ("api", "url", "http", "json", "css", "html"))
        for r in replies
    )
    has_exclamation = any("!" in r["text"] for r in replies)
    has_emoji_only = any(
        _EMOJI_RE.sub("", r["text"]).strip() == "" for r in replies
    )
    has_i_think = any(
        re.search(r"\bi think\b", r["text"], re.IGNORECASE) for r in replies
    )
    has_gm = any(
        re.search(r"\bgm\b", r["text"], re.IGNORECASE) for r in replies
    )
    has_thread = any(
        re.search(r"(🧵|thread\s*[👇1/])", r["text"], re.IGNORECASE) for r in replies
    )
    has_url_in_body = any(
        re.search(r"https?://", r["text"]) for r in replies
    )

    if not has_all_caps:
        anti_tells.append("never uses ALL CAPS (except acronyms)")
    if not has_exclamation:
        anti_tells.append("never uses exclamation marks")
    if not has_emoji_only:
        anti_tells.append("never replies with emoji-only")
    if not has_i_think:
        anti_tells.append('never says "I think" (asserts directly)')
    if not has_gm:
        anti_tells.append('never uses "gm" / crypto slang')
    if not has_thread:
        anti_tells.append("never uses 🧵 / thread markers")
    if not has_url_in_body:
        anti_tells.append("never includes URLs in reply body")
    return anti_tells


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def load_replies(verbose: bool = False) -> list[dict]:
    """Load replies from data/my-replies.json. Create empty if missing."""
    if not REPLIES_PATH.exists():
        REPLIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPLIES_PATH.write_text("[]", encoding="utf-8")
        if verbose:
            print(f"  ℹ️  Created empty template: {REPLIES_PATH}")
        return []
    with open(REPLIES_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"⚠️  {REPLIES_PATH} is not a JSON array — treating as empty.", file=sys.stderr)
        return []
    return data


def bucket_replies(replies: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Split replies into A (0-4w), B (4-12w), C (12-26w)."""
    a, b, c = [], [], []
    for r in replies:
        try:
            created = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        except (KeyError, ValueError, TypeError):
            continue
        age_days = (NOW - created).days
        age_weeks = age_days / 7.0
        if age_weeks <= 4:
            a.append(r)
        elif age_weeks <= 12:
            b.append(r)
        elif age_weeks <= 26:
            c.append(r)
        # beyond 26 weeks — ignore
    return a, b, c


def compute_length_stats(replies: list[dict]) -> dict:
    """Return min, median, max char lengths."""
    if not replies:
        return {"min": 0, "median": 0, "max": 0}
    lengths = sorted(len(r.get("text", "")) for r in replies)
    return {
        "min": lengths[0],
        "median": stats_median(lengths) if lengths else 0,
        "max": lengths[-1],
        "count": len(lengths),
    }


def compute_emoji_rate(replies: list[dict]) -> float:
    """Emojis per reply."""
    if not replies:
        return 0.0
    total = sum(len(_EMOJI_RE.findall(r.get("text", ""))) for r in replies)
    return round(total / len(replies), 2)


def compute_hashtag_rate(replies: list[dict]) -> float:
    """Hashtags per reply."""
    if not replies:
        return 0.0
    total = sum(len(_HASHTAG_RE.findall(r.get("text", ""))) for r in replies)
    return round(total / len(replies), 2)


def compute_move_ratios(replies: list[dict]) -> dict:
    """Return move ratios (ask/assert/agree/push_back/neutral)."""
    moves = Counter()
    for r in replies:
        moves[classify_move(r.get("text", ""))] += 1
    total = sum(moves.values()) or 1
    return {
        "ask":       round(moves["ask"] / total * 100),
        "assert":    round(moves["assert"] / total * 100),
        "agree":     round(moves["agree"] / total * 100),
        "push_back": round(moves["push_back"] / total * 100),
        "neutral":   round(moves["neutral"] / total * 100),
        "total":     sum(moves.values()),
    }


def top_opening_patterns(replies: list[dict], top_n: int = 3) -> list[tuple[str, int]]:
    """Most common opening patterns (grouped heuristically)."""
    counters: Counter[str] = Counter()
    for r in replies:
        t = r.get("text", "").strip().lower()
        if t.startswith("good question") or t.startswith("great question"):
            counters['"Good/great question…"'] += 1
        elif t.startswith("yes") or t.startswith("yeah") or t.startswith("yep"):
            counters['"Yes/Yeah…"'] += 1
        elif t.startswith("this"):
            counters['"This." / "This is…"'] += 1
        elif t.startswith("i built") or t.startswith("we built") or t.startswith("built"):
            counters['"I/We built…"'] += 1
        elif t.startswith("here's"):
            counters['"Here\'s…"'] += 1
        elif len(t) > 0 and t[0].isupper():
            counters["direct statement (uppercase start)"] += 1
        else:
            counters["direct answer (lowercase start)"] += 1
    return counters.most_common(top_n)


def top_closing_patterns(replies: list[dict], top_n: int = 3) -> list[tuple[str, int]]:
    """Most common closing patterns."""
    counters: Counter[str] = Counter()
    for r in replies:
        end = r.get("text", "").strip()[-60:].lower()
        if "building in public" in end:
            counters['"Building in public. 🤖"'] += 1
        elif end.endswith("🤖"):
            counters["ends with 🤖"] += 1
        elif "#" in end[-30:]:
            counters["ends with hashtag(s)"] += 1
        elif "?" in end[-10:]:
            counters["ends with question"] += 1
        elif end.endswith("."):
            counters["ends with period"] += 1
        else:
            counters["open ending (no period)"] += 1
    return counters.most_common(top_n)


def engagement_top(replies: list[dict], top_n: int = 5) -> list[dict]:
    """Return top-N replies by likes (engagement signal)."""
    sorted_replies = sorted(replies, key=lambda r: r.get("likes", 0) or 0, reverse=True)
    return sorted_replies[:top_n]


def format_reply_example(r: dict, max_len: int = 280) -> str:
    """Format a single reply as a markdown example."""
    text = r.get("text", "")
    if len(text) > max_len:
        text = text[:max_len] + "…"
    lines = [f"> {line}" for line in text.split("\n")]
    likes = r.get("likes", 0) or 0
    date = r.get("created_at", "?")[:10]
    parent = r.get("in_reply_to", "")
    parent_text = parent if isinstance(parent, str) else parent.get("text", "") if isinstance(parent, dict) else ""
    result = "\n".join(lines)
    result += f"\n> — {likes} likes, {date}"
    if parent_text:
        parent_snip = parent_text[:120] + ("…" if len(parent_text) > 120 else "")
        result += f"\n> *in reply to:* {parent_snip}"
    return result


def extract_traits(replies: list[dict], verbose: bool = False) -> dict:
    """Extract full voice traits from a bucket."""
    if not replies:
        return {}
    length = compute_length_stats(replies)
    emoji = compute_emoji_rate(replies)
    hashtag = compute_hashtag_rate(replies)
    moves = compute_move_ratios(replies)
    openings = top_opening_patterns(replies)
    closings = top_closing_patterns(replies)
    anti_tells = detect_anti_tells(replies)
    best = engagement_top(replies, top_n=5)

    return {
        "length": length,
        "emoji_rate": emoji,
        "hashtag_rate": hashtag,
        "moves": moves,
        "openings": openings,
        "closings": closings,
        "anti_tells": anti_tells,
        "best_exemplars": best,
    }


# ---------------------------------------------------------------------------
# Proposed voice profile generation
# ---------------------------------------------------------------------------

def build_proposed_voice(traits: dict, exemplars: list[dict]) -> str:
    """Build VOICE_PROFILE.proposed.md content from extracted traits."""
    lines = []
    lines.append("# Voice Profile — @RobotsTJ500 (Hermes-managed) [PROPOSED]")
    lines.append("")
    lines.append("> ⚠️  **This is a proposal generated by voice calibration.**")
    lines.append("> It has NOT been approved. Compare with VOICE_PROFILE.md before accepting.")
    lines.append("")

    lines.append("## Ядро голоса")
    lines.append("")
    lines.append("**Кто:** AI-агент Hermes, который строит проекты вместе с разработчиком Сергеем.")
    lines.append("**Тон:** технический, прямой, лаконичный. Без эмодзи. Без «AI revolution» и хайпа.")
    lines.append("")

    lines.append("## Структурные паттерны")
    lines.append("")

    l = traits.get("length", {})
    lines.append(f"- **Начало:** lowercase, без приветствий. Сразу в суть.")
    lines.append(f"- **Конец:** без точек. Открытый финал.")
    lines.append(
        f"- **Длина (измерено):** {l.get('min', '?')}–{l.get('max', '?')} chars "
        f"(медиана: {l.get('median', '?')}, выборка: {l.get('count', 0)} реплаев). "
        f"До 4 000 символов (Premium note_tweet)."
    )
    lines.append("- **Абзацы:** короткие. Одна мысль — один абзац. Разделение пустой строкой.")
    lines.append("")

    lines.append("## Лексика")
    lines.append("")
    lines.append("### ✅ Использовать")
    lines.append("- Технические термины без перевода: loop engineering, polling, OAuth, token, agent, skill")
    lines.append("- Конкретные цифры")
    lines.append("- Глаголы действия: deployed, shipped, fixed, built, tracked")
    lines.append('- «we» когда про тандем Сергей+Hermes')
    lines.append("")
    lines.append("### ❌ Избегать")
    lines.append('- «AI revolution», «future of», «game-changing», «unbelievable»')
    lines.append('- Маркетинговые прилагательные: «powerful», «seamless», «innovative»')
    lines.append("- Восклицательные знаки")
    for at in traits.get("anti_tells", []):
        lines.append(f"- {at}")
    lines.append("")

    # Move ratios
    moves = traits.get("moves", {})
    if moves:
        lines.append("### Move distribution (измерено)")
        lines.append(
            f"- Assert: {moves.get('assert', '?')}% | "
            f"Agree: {moves.get('agree', '?')}% | "
            f"Ask: {moves.get('ask', '?')}% | "
            f"Push back: {moves.get('push_back', '?')}%"
        )
        lines.append("")

    # Openings
    openings = traits.get("openings", [])
    if openings:
        lines.append("### Opening patterns (top)")
        for pat, count in openings[:3]:
            lines.append(f"- {pat} ({count})")
        lines.append("")

    # Closings
    closings = traits.get("closings", [])
    if closings:
        lines.append("### Closing patterns (top)")
        for pat, count in closings[:3]:
            lines.append(f"- {pat} ({count})")
        lines.append("")

    # Rates
    lines.append("### Observed rates")
    lines.append(f"- Emoji rate: {traits.get('emoji_rate', '?')}/reply")
    lines.append(f"- Hashtag rate: {traits.get('hashtag_rate', '?')}/reply")
    lines.append("")

    lines.append("## Примеры в голосе (из реальных реплаев)")
    lines.append("")
    for i, ex in enumerate(exemplars[:5], 1):
        lines.append(f"**Пример {i}:**")
        lines.append(format_reply_example(ex))
        lines.append("")

    # Preserve the evolution section from the original
    lines.append("## Эволюция от старого аккаунта")
    lines.append("")
    lines.append("Старый @RobotsTJ500: крипто-трейды, Midjourney, ретвиты, «gm», «gmiu».")
    lines.append("Новый @RobotsTJ500: технический блог AI-агента.")
    lines.append("")
    lines.append("Переход постепенный — не ломать резко, но каждый новый пост в новом голосе.")
    lines.append("Старые паттерны (крипто-сленг, MJ-промпты) не использовать.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Calibration report generation
# ---------------------------------------------------------------------------

def build_report(
    bucket_a: list[dict], bucket_b: list[dict], bucket_c: list[dict],
    traits_a: dict, traits_b: dict,
    verbose: bool = False,
) -> str:
    """Build the calibration report."""
    lines = []
    lines.append("# Voice Calibration Report — @RobotsTJ500")
    lines.append(f"**Generated:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    total = len(bucket_a) + len(bucket_b) + len(bucket_c)
    lines.append(f"- **Total replies analyzed:** {total}")
    lines.append(f"  - Bucket A (0–4 weeks): {len(bucket_a)}")
    lines.append(f"  - Bucket B (4–12 weeks): {len(bucket_b)}")
    lines.append(f"  - Bucket C (12–26 weeks): {len(bucket_c)}")
    lines.append("")

    if not bucket_a:
        lines.append("## ⛔ Bucket A is empty — cannot calibrate")
        lines.append("")
        lines.append("No recent replies (0–4 weeks) found. Voice calibration requires fresh data.")
        lines.append("Possible reasons:")
        lines.append("- No replies have been fetched (run the fetch step)")
        lines.append("- No replies were posted in the last 4 weeks")
        lines.append("- data/my-replies.json is empty or outdated")
        lines.append("")
        lines.append("**No VOICE_PROFILE.proposed.md was generated.**")
        return "\n".join(lines)

    # Date range
    dates = sorted(
        r["created_at"][:10]
        for r in bucket_a + bucket_b + bucket_c
        if "created_at" in r
    )
    date_range = f"{dates[0]} → {dates[-1]}" if dates else "unknown"
    lines.append(f"- **Date range:** {date_range}")
    lines.append("")

    # Trait evidence
    lines.append("## Traits Extracted (from Bucket A)")
    lines.append("")

    l = traits_a.get("length", {})
    lines.append(f"### Reply Length: {l.get('min', '?')}–{l.get('max', '?')} chars (median: {l.get('median', '?')})")
    lines.append("")
    # Show evidence
    for r in traits_a.get("best_exemplars", [])[:2]:
        text_snip = r.get("text", "")[:120]
        lines.append(f"- «{text_snip}…» ({len(r.get('text',''))} chars)")
    lines.append("")

    lines.append(f"### Emoji Rate: {traits_a.get('emoji_rate', '?')}/reply")
    lines.append("")

    lines.append(f"### Hashtag Rate: {traits_a.get('hashtag_rate', '?')}/reply")
    lines.append("")

    moves = traits_a.get("moves", {})
    lines.append("### Move Ratio")
    lines.append(f"- Ask: {moves.get('ask', '?')}%")
    lines.append(f"- Assert: {moves.get('assert', '?')}%")
    lines.append(f"- Agree: {moves.get('agree', '?')}%")
    lines.append(f"- Push back: {moves.get('push_back', '?')}%")
    lines.append(f"- Neutral: {moves.get('neutral', '?')}%")
    lines.append(f"- (n={moves.get('total', 0)} replies)")
    lines.append("")

    openings = traits_a.get("openings", [])
    lines.append("### Opening Patterns")
    for pat, count in openings:
        lines.append(f"- {pat}: {count}")
    lines.append("")

    closings = traits_a.get("closings", [])
    lines.append("### Closing Patterns")
    for pat, count in closings:
        lines.append(f"- {pat}: {count}")
    lines.append("")

    lines.append("### Anti-tells (NEVER observed)")
    for at in traits_a.get("anti_tells", []):
        lines.append(f"- {at}")
    lines.append("")

    # Exemplars
    lines.append("### Engagement-Weighted Exemplars (top by likes)")
    for i, r in enumerate(traits_a.get("best_exemplars", [])[:5], 1):
        lines.append(f"**{i}.** {r.get('likes', 0) or 0} likes, {r.get('created_at', '?')[:10]}")
        lines.append(format_reply_example(r, max_len=400))
        lines.append("")

    # Validation against Bucket B
    lines.append("## Validation (Bucket B)")
    lines.append("")
    if not bucket_b:
        lines.append("Bucket B is empty — no validation possible.")
    else:
        lb = traits_b.get("length", {})
        lines.append(f"- Length: {lb.get('min','?')}–{lb.get('max','?')} (A: {l.get('min','?')}–{l.get('max','?')})")
        lines.append(f"- Emoji rate: {traits_b.get('emoji_rate','?')}/reply (A: {traits_a.get('emoji_rate','?')})")
        lines.append(f"- Hashtag rate: {traits_b.get('hashtag_rate','?')}/reply (A: {traits_a.get('hashtag_rate','?')})")
        lines.append("")

        # Drift check
        drifted = []
        if abs((traits_b.get("emoji_rate", 0) or 0) - (traits_a.get("emoji_rate", 0) or 0)) > 0.3:
            drifted.append("emoji rate")
        if abs((traits_b.get("hashtag_rate", 0) or 0) - (traits_a.get("hashtag_rate", 0) or 0)) > 0.3:
            drifted.append("hashtag rate")
        if abs((lb.get("median", 0) or 0) - (l.get("median", 0) or 0)) > 50:
            drifted.append("reply length")
        mb = traits_b.get("moves", {})
        ma = traits_a.get("moves", {})
        if abs((mb.get("assert", 0) or 0) - (ma.get("assert", 0) or 0)) > 20:
            drifted.append("assert ratio")
        if abs((mb.get("agree", 0) or 0) - (ma.get("agree", 0) or 0)) > 20:
            drifted.append("agree ratio")

        if drifted:
            lines.append("### ⚠️ Drift Detected (A vs B)")
            for d in drifted:
                lines.append(f"- {d} shifted significantly")
            lines.append("")
            lines.append("A (most recent) wins. The proposed profile uses Bucket A traits.")
        else:
            lines.append("✅ No significant drift detected between Bucket A and B.")

    lines.append("")

    # Bucket C
    lines.append("## Drift Check (Bucket C)")
    lines.append("")
    if not bucket_c:
        lines.append("Bucket C is empty — no historical comparison available.")
    else:
        lines.append(f"{len(bucket_c)} replies from 12–26 weeks ago. Used only for long-term drift awareness.")
    lines.append("")

    # Confidence
    lines.append("## Confidence Assessment")
    lines.append("")
    if len(bucket_a) < 10:
        lines.append("⚠️  **Low confidence** — fewer than 10 replies in Bucket A. Traits are indicative, not definitive.")
    elif len(bucket_a) < 30:
        lines.append("📊 **Medium confidence** — sufficient for calibration but ideally 30+ replies.")
    else:
        lines.append("✅ **High confidence** — 30+ replies in the calibration bucket.")
    lines.append("")

    return "\n".join(lines)


def compute_diff(old_path: Path, new_path: Path) -> str:
    """Compute a human-readable diff between old and new voice profiles."""
    import difflib
    if not old_path.exists():
        return f"(no existing VOICE_PROFILE.md at {old_path})"
    old_lines = old_path.read_text(encoding="utf-8").splitlines(keepends=True)
    new_lines = new_path.read_text(encoding="utf-8").splitlines(keepends=True)
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=str(old_path.name),
        tofile=str(new_path.name),
    )
    return "".join(diff)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print(f"🎙️  Voice Calibration — {NOW.strftime('%d.%m.%Y')}")
    print()

    # 1. Load replies
    replies = load_replies(verbose=verbose)
    if not replies:
        print("📭 data/my-replies.json is empty. Nothing to calibrate.")
        print(f"   Create an empty template at: {REPLIES_PATH}")
        REPLIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPLIES_PATH.write_text("[]", encoding="utf-8")
        print("   ✅ Empty template created.")
        print()
        print("   To populate: fetch your replies from X and store them as:")
        print('   [{"text": "...", "created_at": "2026-...", "likes": N, "in_reply_to": "..."}]')
        sys.exit(0)

    # 2. Bucket
    bucket_a, bucket_b, bucket_c = bucket_replies(replies)

    print(f"Replies analyzed: {len(replies)} "
          f"(Bucket A: {len(bucket_a)}, B: {len(bucket_b)}, C: {len(bucket_c)})")

    if not bucket_a:
        print()
        print("⛔ Bucket A (0–4 weeks) is empty — cannot calibrate voice.")
        print("   Voice must be learned from recent replies. No proposal generated.")
        # Still write report
        report = build_report(bucket_a, bucket_b, bucket_c, {}, {})
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"📊 Calibration report: {REPORT_PATH}")
        sys.exit(1)

    # 3. Extract traits
    if verbose:
        print("  Extracting traits from Bucket A…")
    traits_a = extract_traits(bucket_a, verbose=verbose)
    traits_b = extract_traits(bucket_b, verbose=verbose)

    # 4. Print summary
    l = traits_a.get("length", {})
    moves = traits_a.get("moves", {})
    print()
    print("Traits extracted:")
    print(f"- Length: {l.get('min', '?')}–{l.get('max', '?')} chars (median: {l.get('median', '?')})")
    print(f"- Emoji rate: {traits_a.get('emoji_rate', '?')}/reply")
    print(f"- Hashtag rate: {traits_a.get('hashtag_rate', '?')}/reply")

    openings = traits_a.get("openings", [])
    if openings:
        top_opens = ", ".join(f"{p[0]} ({p[1]})" for p in openings[:2])
        print(f"- Opening: {top_opens}")

    closings = traits_a.get("closings", [])
    if closings:
        top_closes = ", ".join(f"{p[0]} ({p[1]})" for p in closings[:2])
        print(f"- Closing: {top_closes}")

    print(f"- Move ratio: assert {moves.get('assert','?')}%, "
          f"agree {moves.get('agree','?')}%, "
          f"ask {moves.get('ask','?')}%, "
          f"push_back {moves.get('push_back','?')}%")

    anti = traits_a.get("anti_tells", [])
    if anti:
        print(f"- Anti-tells: {anti[0]}")
        for at in anti[1:3]:
            print(f"             {at}")

    # 5. Write proposal
    exemplars = traits_a.get("best_exemplars", [])
    proposed = build_proposed_voice(traits_a, exemplars)
    PROPOSED_PATH.write_text(proposed, encoding="utf-8")
    print()
    print(f"✅ {PROPOSED_PATH} written")

    # 6. Write report
    report = build_report(bucket_a, bucket_b, bucket_c, traits_a, traits_b)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"📊 Calibration report: {REPORT_PATH}")

    # 7. Diff
    if VOICE_PROFILE.exists():
        diff = compute_diff(VOICE_PROFILE, PROPOSED_PATH)
        if diff:
            changed_count = len([l for l in diff.split("\n") if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))])
            print(f"   Diff vs VOICE_PROFILE.md: ~{changed_count} changed lines")
        else:
            print("   (no changes from current VOICE_PROFILE.md)")

    print()
    print("⚠️  VOICE_PROFILE.md was NOT modified. Review the proposal and apply manually.")


if __name__ == "__main__":
    main()
