# MoA Review 1 — Under the Hood (2026-10-31, text v1_en + cover v1)

**Verdict: CHANGES_REQUIRED**

## 1. Voice — PASS
- First-person I/we present ("We read ours", "We ran the audit") — consistent.
- No ALL-CAPS in first 160 chars. Hook: "X now publishes a transparency report on how it limits your reach. We read ours the same week — clean." — calm, factual, no hype words.
- Honest downsides present: retrospective lag ("cannot warn you the same day", "a week after you noticed") — the post explicitly concedes the report's weakness. Good.

## 2. ANTI-AD — PASS (borderline OK)
- No landing-page tone, no slogans, no CTA. "What to steal" is a takeaway list, not promo.
- "Building in public. 🤖" is a signature, not self-promo. OK.
- Self-promo has scar tissue (the lag limitation, "feeling → claim" framing), so no ad smell.

## 3. MENTIONS — FAIL
- @XOpenSource is listed in the file header comments but NEVER in the post body. The 30.10 announcement is their post; the "new part (yesterday)" sentence credits nobody.
- **Fix:** in line 10, attribute the update: e.g. "The new part @XOpenSource shipped yesterday: it now names the specific posts…"

## 4. ФАКТ-СВЕРКА — CHANGES_REQUIRED (1 omission, rest accurate)
- Cadence: "last complete month, lands about ten days later" ✓ (monthly, retrospective, ~10th).
- Access: "account older than a year with ten posts in the report month" ✓ (≥1 год, ≥10 постов/мес).
- 7-day isFinal window ✓ ("under observation for seven days before it is final"), and correctly used as appeal window in bullets.
- <5% threshold ✓ ("if fewer than 5% of your posts carry a label").
- **Effects — INCOMPLETE:** draft only says labels "hid posts from recommendations to non-followers". Source: label = warning shown to non-followers + блок лайк/реплай/репост не-фолловерами. The engagement block is a material effect and is missing from the body.
- **Fix:** line 10 → "…with their effects: a warning shown to non-followers and like/reply/repost blocked for them."
- Launched 13.08 / extended 19 & 24.09: not claimed in draft — no invented history ✓. Our 31.10 clean check matches owner's manual verification ✓.

## 5. Text + cover pair — PASS (minor)
- Cover metaphor (opening the machine to reveal an official graded report) = thesis "hiding is now documented and downloadable". Metaphor carries the thesis, doesn't parrot the hook verbatim. ✓
- Minor nits: "PERFORMANCE REVIEW – A+" is invented flavor (we got "clean", not a grade) — acceptable as visual metaphor but slightly oversells; "HIDDEN PARAMETERS" is garbled AI-artifact text and unreadable at thumbnail size — cosmetic only.

## 6. Structure + value test — PASS
- Hook → what it is → fine print → how to use it (audit vs monitor) → our result → takeaways → closing insight. Complete argument arc, actionable ("x.com/i/under_the_hood, download the JSON, archive it").
- Closing line ("feeling into a claim you can check") earns the read. No filler.

## Required fixes (minimal)
1. Add @XOpenSource attribution in the body (line 10).
2. Complete the label effects: warning to non-followers + engagement block (like/reply/repost).
3. (Optional) Consider whether "A+" on the cover contradicts "clean / no labels" story — recommend regenerating without the grade, or accept as metaphor.
