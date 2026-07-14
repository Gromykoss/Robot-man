---
name: viral-scorer
description: "Score a post on hook strength, engagement potential, and virality using MoA (Grok 4.5 reference + DeepSeek aggregator). Returns BURN/REWRITE/KEEP verdict."
version: 1.0.0
author: Robot-man
metadata:
  robot-man:
    type: scoring
    requires: [moa, xai, deepseek]
---

# Viral Scorer

Scores a draft post on three dimensions (1-10) using the `viral-score` MoA preset (Grok 4.5 as reference for real-time X awareness, DeepSeek as aggregator for structure analysis).

## Usage

```bash
# Via MoA preset
/moa viral-score

# Pipe the post text as the query
```

## Scoring Dimensions

### 1. Hook (1-10)
- Does the first sentence stop the scroll?
- Is there a specific, concrete opening (not generic)?
- Does it create curiosity gap?

**1-3:** Generic opener, no hook
**4-6:** Solid hook, competes in feed
**7-10:** Scroll-stopping, immediate intrigue

### 2. Engagement Potential (1-10)
- Does it invite replies / debate / saves?
- Is there an actionable takeaway?
- Specific numbers or data points?

**1-3:** Read-and-scroll, no reason to engage
**4-6:** Valuable enough for like/save
**7-10:** Reply-bait, shareable, quotable

### 3. Virality (1-10)
- Does it tap a current trend / conversation?
- Would someone outside the niche care?
- Emotional resonance (surprise, delight, frustration)?

**1-3:** Pure personal update, niche-only
**4-6:** Some cross-niche appeal
**7-10:** Trend-jacking potential, high shareability

## Verdict

| Total Score | Verdict |
|-------------|---------|
| > 24 | **BURN** — ready to post immediately |
| 18-24 | **KEEP WITH EDITS** — fix weak dimensions |
| < 18 | **REWRITE** — too weak, start over |

## Scoring Prompt

When scoring, pass:

```
Score this @RobotsTJ500 post on:
1. Hook (1-10): {hook_dimensions}
2. Engagement Potential (1-10): {engagement_dimensions}
3. Virality (1-10): {virality_dimensions}

Total: __/30
Verdict: BURN / KEEP WITH EDITS / REWRITE

Weakest dimension: __
Suggested fix: __
```
