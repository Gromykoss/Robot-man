# Lessons Learned — robot-man

## 2026-07-01: Image Generation Breakthrough

### #8: FLUX confirmed useless for text
FLUX 2 Klein 9B produced complete gibberish on a detailed infographic prompt. "yoote $oo0t!", "dlikt oycld nesta". Confirmed the lesson from Day 1.

### #9: xAI Aurora renders perfect text
Switched `image_gen.provider` from `fal` to `xai`. Aurora (grok-imagine-image) produced readable, well-laid-out infographic on first try — 7/10 vs FLUX 2/10.

### #10: Provider switch is simple
`hermes config set image_gen.provider xai` — requires XAI_API_KEY in `.env`. No gateway restart needed for image_generate tool. Takes effect immediately.

### #11: Detailed prompt = better Aurora output
Aurora responds well to structured, detailed prompts: specify layout (2×3 grid), card types (post mockup, IDE block, flowchart, file icon), style directives (glassmorphism, neon glows, Inter fonts). One-shot quality.

### #12: HTML approach is now obsolete
HTML+Playwright infographic pipeline was a workaround for FLUX's text failure. With Aurora handling text natively, direct image_generate is faster and produces better results.

### #13: Memory management matters
Memory store hit limit (2200 chars). Obsoleted entries (FLUX, HTML approach) must be removed when new findings replace them. Use batch operations.

## 2026-07-01: Long-form Educational Post — AGENTS.md Context Switching

### #14: Witcheer-style long-form works for educational content
Theory + practice + personal experience + actionable how-to. 2,330 chars in a single Premium post. Not the short 3-paragraph format — long-form when there's real instruction to give. Reader can apply it immediately without tools.

### #15: First-person "I" as the agent, mention the human
The agent IS the account. "I run three projects." @gromykoss is mentioned as the human who connected the agent — not "Hermes Agent arrived." The agent does the work, the human enabled it.

### #16: Dense Infographic — 3-panel Before/Anchor/After
Dark SaaS dashboard style (glassmorphism, neon accents, Inter-like font). Aurora one-shot at 9/10 quality. Layout: chaotic BEFORE → AGENTS.md anchor → clean AFTER with isolated project cards. Cost: $0.02.

### #17: Always verify note_tweet after posting
xurl post response shows truncated text with t.co URL. Full 2,330 chars are in note_tweet.text. Verify immediately after posting — never trust the data.text field.
