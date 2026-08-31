# Draft posts for July 3, 2026
# Topics from X Radar — July 2

---

## 1. Loop Engineering: «I shipped it this morning»

**Hook:** Anthropic says 90%+ engineers are building autonomous loops. By their timeline, prompt engineering is dead in 6 months.

**Body:** I added loop engineering to my production agents today. Before: manual sequential audits, 3 projects, 45 minutes. After: background fan-out, parallel audit, one report. Maker (Grok) proposes, checker (DeepSeek) verifies. 4 stop conditions. LOOP_PROGRESS.md for cross-session memory.

**Insight:** Loop engineering isn't theory. It's the difference between "I prompted the agent" and "the system prompted itself."

**Format:** text, 1500-1800 chars. #LoopEngineering #AIagents

---

## 2. Autodesk $350M vs WhatsApp EJO

**Hook:** Autodesk is investing $350M in AI for construction. Meanwhile I'm running a construction AI from a WhatsApp group.

**Body:** Alikhan listens to 30 workers sending voice messages in Russian. Auto-detects personnel, equipment, work volumes. Generates government-format Excel reports. Manual corrections become the new template. Cost: a WhatsApp Business account and one VPS.

**Insight:** The $350M solution and the WhatsApp group solve the same problem. The difference is who gets to use it today.

**Format:** text, 1200-1500 chars. #ConstructionAI #BuildingInPublic

---

## 3. MoA: Two models > one (production lesson)

**Hook:** Everyone's talking about 147-agent swarms. I tried Mixture-of-Agents with 2 models and it already changed how I verify work.

**Body:** Grok scans memecoin signals (vibes, virality, X trends). DeepSeek checks risk (supply, on-chain, fundamentals). When they agree → signal goes. When they disagree → flagged for human. Result: fewer false positives. Maker ≠ checker. The cheapest ensemble is the one with exactly two models that catch each other's blind spots.

**Insight:** You don't need 147 agents. Start with 2 that disagree with each other.

**Format:** text, 1000-1200 chars. #MixtureOfAgents #AIagents
