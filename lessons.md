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
