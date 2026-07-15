---
name: build-blog-writer
description: Turns raw build notes and CHRONOLOGY entries into War Story posts for @RobotsTJ500. Captures the multi-project building-in-public voice.
version: 1.0.0
category: robot-man
---

# Build Blog Writer — Automated War Story Generator

## Trigger

Run every 3 days via cron. Agent asks: "What did you build in the last 3 days?" User dumps raw notes in Telegram. Agent runs this skill and returns a draft post.

## Voice (extracted from @RobotsTJ500 published posts)

- First-person "I", English only
- Practical guide > report — the reader learns something
- Specific numbers and concrete steps (not "we fixed things", but "fixed 3 bugs across 2 repos, 28 commits, 16/16 audit PASS")
- Structure: Problem → What broke (with numbers) → How I fixed it (3-5 steps) → Lesson learned → "Building in public. 🤖" + 3-4 hashtags
- No emojis in body, no URLs in body, no marketing fluff
- Max 4000 chars (Premium note_tweet)

## Source Material (what to read)

This skill reads from:

1. **CHRONOLOGY.md** files in each project — the raw build log:
   - `/home/hermes-workspace/hermes-agent-lab/CHRONOLOGY.md`
   - `/home/hermes-workspace/gooolag/CHRONOLOGY.md`
   - `/home/hermes-workspace/Alikhan-migration/CHRONOLOGY.md`
   - `/home/hermes-workspace/rab9/CHRONOLOGY.md`
   - `/home/hermes-workspace/robot-man/CHRONOLOGY.md`

2. **Published posts** — for voice calibration:
   - `/home/hermes-workspace/robot-man/published_posts.jsonl` (last 5 posts)

3. **User's raw notes** — what the user sends in Telegram when the cron asks

## Process

### Step 1: Gather Updates
Read the last 3 days from all 5 CHRONOLOGY.md files. Extract:
- Date of each change
- What was done (the "Что сделано" sections)
- Bugs fixed (the "Исправление" / "Fix" sections)
- Numbers that matter: commits, tests passed, bugs squashed, users added, lines changed

### Step 2: Pick the Most Interesting Story
From the gathered data, pick ONE story that has:
- A clear problem → fix arc
- Specific numbers
- A lesson that generalizes beyond our setup
- Priority: security fixes > automation wins > architecture improvements > routine maintenance

### Step 3: Write in @RobotsTJ500 Voice
Use the voice profile from `/home/hermes-workspace/robot-man/VOICE_PROFILE.md`:
```
- First-person "I", English only
- Practical guide > report
- "Building in public. 🤖" — closing
- #hashtags required, no URL in body
```

### Step 4: Structure the Post

```
[HOOK — one sentence that makes you want to read]

[PROBLEM — what happened, with numbers]

[FIX — 3-5 concrete steps I took]

[LESSON — one insight that generalizes]

[CLOSING]
Building in public. 🤖

#[hashtag1] #[hashtag2] #[hashtag3] #[hashtag4]
```

### Step 5: MoA Verification
Run `/moa deepseek-xai` on the draft. Both models must agree. If not — rewrite.

### Step 6: Image
Generate a cover image using `loop-image-gen` (landscape 16:9). Goal: 8-10/10 scroll-stopper.

### Step 7: Show to User
Present text + image to user for approval. Only publish after explicit "ok".

## Anti-Patterns to Avoid

- "Today I worked on..." — weak hook. Use the result or the problem as hook
- Listing all projects — pick ONE story
- No numbers = no post. If you can't quantify it, find a different story
- URL in the post body
- More than 4 hashtags
- Posting without user approval

## Example (from our actual build log)

```
HOOK: My security audit scored 50%. Then I fixed 8 things in one session.

PROBLEM: Docker ran :latest images. Observability was wide open on 0.0.0.0.
Grafana password sat in plaintext Git history. 13 docs, 10 sources of truth.

FIX (5 steps):
1. Rotated Grafana password, gitignored the env file
2. Bound Prometheus + Grafana to 127.0.0.1 only
3. Pinned Docker images to specific versions (no :latest)
4. Added no-new-privileges, memory limits, read-only rootfs
5. Built a pre-commit secret scanner — blocks commits with API keys

RESULT: Security audit went from 50% to 100% in 3 commits. 16/16 checks pass.
5 tests, 0 failures. Every commit now scanned for secrets before it lands.

LESSON: Security isn't a feature you add. It's a pipeline you build.
If it's not automated, it doesn't exist.

Building in public. 🤖

#HermesAgent #DevSecOps #BuildingInPublic #Automation
```

## Cron Job Setup

```
cronjob action=create
name="Build Blog — every 3 days"
schedule="0 14 */3 * *"
prompt="Ask the user: 'What did you build in the last 3 days?' When they send notes, run the build-blog-writer skill and generate a draft post. Send the draft + image to Telegram for review."
skills=["build-blog-writer"]
deliver="origin"
workdir="/home/hermes-workspace/robot-man"
```

## Verification

After generating a post:
1. Check: is there a hook? (first line should grab attention)
2. Check: are there numbers? (at least 2-3 specific metrics)
3. Check: does the lesson generalize? (useful to someone outside our setup)
4. Check: voice matches @RobotsTJ500
5. Run MoA — both models must agree
6. Verify image with vision_analyze — 8/10 minimum
