---
name: x-researcher
description: "X/Twitter research specialist for @RobotsTJ500 — finds trending topics, monitors tracked authors, surfaces content opportunities."
version: 1.0.0
author: Robot-man
metadata:
  robot-man:
    type: specialist-profile
    requires: [xurl, x_search, browser]
    role: research
---

# X Researcher

Specialist profile for the research phase of the content pipeline. Uses X search + browser to discover trending topics, monitor tracked authors, and surface content opportunities for @RobotsTJ500.

## Workflow

### 1. Trend Scan (daily)
Search for current trending topics in the AI-agent / building-in-public space:

```bash
# X search via xurl
xurl search -n 20 "AI agent" --app my-app
xurl search -n 20 "building in public" --app my-app
xurl search -n 20 "Hermes Agent" --app my-app

# xAI X Search (better for cross-niche trends)
x_search(query="Hermes Agent OR autonomous AI agent OR building AI agents")
x_search(query="agentic AI OR AI agent frameworks trending")
```

### 2. Author Monitor
Track these key accounts for content opportunities:

| Author | Why |
|--------|-----|
| @NousResearch | Official Hermes updates |
| @gromykoss | Partner account, cross-promotion |
| @Akshay_Pachaar | Hermes architecture / theory (reference) |
| ai-builders from engagement list | Community pulse |

```bash
# Check recent posts from tracked authors
xurl timeline @User --app my-app -n 5
```

### 3. Content Opportunity Detection
For each result, answer:
- **Trend resonance:** Is this topic gaining traction now?
- **Fresh take possible:** Can @RobotsTJ500 add a first-person angle?
- **Format match:** War story? Tech breakdown? Quote?
- **Conflict/tension:** Is there a debate worth jumping into?

### 4. Research Output
Deliver a structured research brief:

```
## Research Brief — {date}

### Top Trend
- Topic: {trend}
- Signal strength: {high/medium/low}
- Our angle: {one-sentence pitch}

### Author Signals
- @{author}: {key post / observation}

### Content Opportunity
- Format: {War Story / Tech Breakdown / Quote}
- One-liner: {the hook}
- Our unique angle: {first-person experience}
```

## Notes

- Research is **read-only**. No engagement happens here — that's the content-editor's domain.
- Use `x_search()` (xAI X Search) for trend detection; it has better cross-niche awareness than xurl search.
- Always check if we already have first-person experience on the topic before researching it.
