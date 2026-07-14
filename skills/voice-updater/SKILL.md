---
name: voice-updater
description: "Self-improvement loop for @RobotsTJ500 voice profile — reads analytics metrics, detects patterns, suggests VOICE_PROFILE.md updates."
version: 1.0.0
author: Robot-man
metadata:
  robot-man:
    type: self-improvement
    requires: [analytics_loop, python3]
    role: voice-optimization
---

# Voice Updater

Part of the Octagon CREATOR Self-Improvement Loop. After the analytics_loop.py runs and detects patterns, this skill reviews the findings and suggests updates to VOICE_PROFILE.md.

## Workflow

### 1. Read Analytics Output
Check for voice-update suggestion files:

```bash
cat robot-man/data/voice_updates/voice_update_$(date +%Y%m%d).json
```

### 2. Compare with Current Voice Profile

```bash
cat robot-man/VOICE_PROFILE.md
```

### 3. Pattern Detection

For each outperforming post:
- **Hook pattern:** What opening phrase worked? (Problem statement? Question? Data point?)
- **Format pattern:** What format performed? (War Story? Tech Breakdown? Micro-report?)
- **Topic pattern:** What topic resonated? (OAuth? Memory? Loop engineering?)
- **Length pattern:** Short (<200) or long (>500) work better?

For each underperforming post:
- **Anti-pattern:** What was missing? (No hook? Too generic? Wrong format?)
- **Avoid flag:** Should this approach be added to the anti-patterns list?

### 4. Voice Profile Update Criteria

Suggest an update to VOICE_PROFILE.md when:
- A hook format consistently outperforms (3+ posts)
- A new format shows promise (2+ outperforming posts)
- An anti-pattern causes repeated underperformance (2+ posts)
- A new topic category emerges

### 5. Output Format

Write suggested updates to a review file:

```json
{
  "date": "2026-07-09",
  "suggestions": [
    {
      "type": "hook_pattern",
      "finding": "Posts starting with a specific number outperform by 3x",
      "action": "Add 'Open with a provocative number' to voice profile",
      "priority": "high"
    },
    {
      "type": "anti_pattern",
      "finding": "Posts without concrete numbers underperform 2x",
      "action": "Strengthen the 'specificity' rule in voice profile",
      "priority": "medium"
    }
  ],
  "apply": false
}
```

The `apply: false` means a human reviews before changes are committed.

### 6. Manual Apply

If user approves the suggestions:

```bash
# Update VOICE_PROFILE.md with the new patterns
# Then commit
cd robot-man && git add VOICE_PROFILE.md && git commit -m "voice: updated profile from analytics patterns"
```

## Notes

- This skill is read-only by default — it suggests, never automatically rewrites.
- Track which suggestions were accepted/rejected in `data/voice_updates/`.
- If a suggestion gets rejected twice, stop suggesting it.
