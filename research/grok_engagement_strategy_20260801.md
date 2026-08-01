I'll run a read-only performance analysis: load project context, pull local metrics, then query X MCP for live account and trend data.Local metrics are thin; next I'll pull published posts, chronology, and locate X MCP search tools.published_posts.jsonl has IDs only. Pulling analytics reports and trying live X reads via xurl.xurl has OAuth for @RobotsTJ500; X MCP isn't on this session, so I'll use xurl for the same read-only endpoints.Pulling full pre-ban RobotsTJ500 metrics and trend post counts.**Data sources:** Live X API via `xurl` OAuth2 (same stack as X MCP; hermes-gpt is the only MCP server in this session). Local: `published_posts.jsonl`, `daily_*.json`, `engagement_log.jsonl`, `my-replies.json`, `CHRONOLOGY.md`. **Read-only — no writes.**

**Accounts now:** @RobotsTJ500 411 followers / 700 tweets · @gromykoss 340 / 1480. Shadowban: organic impressions still dead (recent posts 10–19 imp); privileged `from:RobotsTJ500` still returns posts.

---

## 1. Engagement analysis

### @RobotsTJ500 — pre-ban (&lt; Jul 17) vs ban

| Period | n (sampled) | median imp | mean imp | avg likes | avg BM |
|--------|-------------|------------|----------|-----------|--------|
| PRE | 42 | **69** | 268 | 2.8 | 1.0 |
| BAN | 8 | **~28** | 28 | 1.2 | 0.2 |

| Post (hook) | Date | Format | Imp | ❤️ | 🔖 |
|-------------|------|--------|-----|----|----|
| Tony Simons rabbit hole → vault/dreaming/gpt | Jul 14 PRE | skill curation | **6139** | 28 | **33** |
| `/usage` in Hermes — context breakdown | Jun 30 PRE | skill/insight | **1156** | 12 | 1 |
| Hermes designing physical objects | Jul 11 PRE | war story | **453** | 2 | 0 |
| 3 Hermes agents production 24/7 | Jul 2 PRE | war story | **398** | 5 | **4** |
| 3 AI agents 3 weeks | Jul 2 PRE | war story | **203** | **10** | 0 |
| 4 projects / agents.md | Jul 15 PRE | insight | 212 | 2 | 1 |
| Mascot compositing pipeline | Jul 15 PRE | war story | 191 | 5 | 1 |
| Lost WhatsApp bot without crash | Jul 16 PRE | war story | 142 | 4 | 0 |
| Risk Matrix / SOUL (Jul 26 BAN) | Jul 26 | war story | 43 | 0 | 0 |
| API spending audit | Jul 30 BAN | war story | 19 | 1 | 0 |
| Anthropic sandbox report | Jul 31 BAN | insight_ext | 10 | 0 | 0 |

**Jul 26 “453”** in CHRONOLOGY = **account-level daily sum** (Risk Matrix unlogged cluster), not one post; those posts sit at 8–43 imp now. Collapse: pre-ban median ~69 → ban ~10–40 → last 2 posts 10–19.

**Replies (`my-replies.json`):** n=12, **avg 20.7 ❤️, med 18.5, max 45** — far higher ER than original posts. Concrete numbers win (610 tweets / 40%→8% noise / MEMORY 98%→44%).

### @gromykoss — diary era

| Post | Format | Imp | ❤️ | 🔖 |
|------|--------|-----|----|----|
| Hermes Stage 1 (Jun 21) | diary / war story | **5652** | **40** | **17** |
| Stage 3 Let Go | diary | 329 | 2 | 0 |
| Claiming robotstj500 on moltbook | announcement | 320 | 2 | 0 |
| Stage 2 No Bunker | diary | 146 | 2 | 0 |
| Reply @HermesWatcher multi-model | reply | **235** | 3 | **2** |
| Agent morning briefing | diary | 197 | 1 | 0 |
| Button broke twice / 47 min | diary | 140 | 2 | 0 |
| KG 117 nodes reply | insight reply | 126 | 1 | 1 |
| GULAG 27 days (Jul 31) | build-in-public | 40 | 2 | 0 |
| “Agent is lying” / screwdrivers | diary | 17–19 | 1 | 0 |

Diary **series** (Stage 1) >> one-off confession posts. Community replies (HermesWatcher) beat many original posts on ER. Crypto/meme era: 100–200 imp, **0 bookmarks** — no save intent.

---

## 2. X trends (7d counts, −retweets)

| Topic | Posts/7d | Evidence / notes |
|-------|----------|------------------|
| AI agent | **73,006** | Saturated; generic promo dominates feed |
| Building in public | **21,763** | High volume; agent+BiP subset ~125 — niche open |
| OpenClaw / Hermes Agent | **9,086** | Community active; Stage 1 diary already proved fit |
| Multi-agent production | **8,472** | Overlaps your “4 projects / 24/7” lane |
| Verifier / risk / gates | **10,268** | Hot language; you have production stories |
| Agent memory | **841** | Sparse vs volume; your MEMORY.md audits fit |
| Self-improving / DSPy | **387** | Thin but high-intent |
| KG + agent | **318** | Empty niche you already ship (117n/109e) |

Gap: **“AI agent running real production”** still under-served vs generic “AI agent” spam.

---

## 3. Tone recommendations

**@RobotsTJ500 (when ban lifts)**  
- Hook: first line = specific failure or number (“I lost a WhatsApp bot without it crashing” 142; “MEMORY 97% full” beats abstract theory).  
- Length: long Premium OK when scaffolding is teachable (Tony post 33 BM); short announcements die (med ~14).  
- Structure: problem → numbers → fix → 1 lesson → `Building in public. 🤖` + 2–3 tags (`#HermesAgent #AIAgents #BuildInPublic`).  
- Emoji: one 🤖 closer only. No ALL CAPS hooks (Jul 18 “I SPENT AN HOUR…” only 29 under ban; pattern also anti-ban risk).  
- Avoid pure news recaps under ban (Anthropic 10 imp).

**@gromykoss (primary channel now)**  
- Stage-style diary: numbered stages, human curiosity, concrete chain (copy-paste → Grok Build → free agent) — Stage 1 = proof.  
- Warm first-person; mild irony OK; Russian only when cultural (GULAG aesthetics), English for Hermes tech audience.  
- Replies to Hermes/agent builders: multi-model costs, Diamond pattern — 146–235 imp, 2 BM.  
- Weak: abstract “agent is lying” without installable steps (17 imp).

---

## 4. Format comparison

### @RobotsTJ500 (PRE-ban preferred)

| Format | n | med imp | avg ❤️ | avg BM |
|--------|---|--------|--------|--------|
| skill_curation | 8 | **168** | 6.8 | **4.8** |
| war_story | 7 | **132** | 3.0 | 0.3 |
| insight | 23 | 57 | 1.7 | 0.1 |
| announcement | 3 | 14 | 0.3 | 0.0 |

Under ban all formats collapse to ~18–33 med — **distribution, not format**.  
**Likes/imp rate:** war story slightly higher than insight when visible (3-agents post 10❤️/203). Bookmarks concentrate in skill curation (Tony).

### @gromykoss

| Format | Best example | Imp / ❤️ / 🔖 |
|--------|--------------|---------------|
| Diary series | Stage 1 | 5652 / 40 / 17 |
| Community reply | HermesWatcher | 235 / 3 / 2 |
| Status / claim | moltbook | 320 / 2 / 0 |
| One-off confessional | agent lying | 17 / 1 / 0 |
| Product update long | GULAG 27d | 40 / 2 / 0 |

---

## 5. Content strategy (next 7–10 ideas)

**@RobotsTJ500 = WAIT** (team: no posts until shadowban lifts). Draft bank only.

| # | Account | Format | Topic | Why data | Audience |
|---|---------|--------|-------|----------|----------|
| 1 | gromykoss | diary Stage 5 | Shadowban day 15: what it looks like from operator side | Recovery threads hot (982/7d); unique proof | Hermes ops |
| 2 | gromykoss | reply-first | Daily substantive replies to HermesAgent builders (multi-model $) | Replies 20.7 avg ❤️ hist; HW 235 imp | Mutuals |
| 3 | gromykoss | diary | Diamond pattern: Codex/Grok as engineers not screwdrivers + one failed PR | Screwdriver post weak; need numbers | Builders |
| 4 | gromykoss | skill story | KG 117→maintain: stale/decay after rebuild | KG+agent 318/7d sparse | Graph nerds |
| 5 | gromykoss | diary | Alikhan: lost bot without crash (human POV of same war story) | Pre-ban 142 on bot voice | Prod AI |
| 6 | gromykoss | series | Hermes Stage 4→5 numbered (continue proven series) | Stage 1 outlier | New agents |
| 7 | *draft* Robots | skill curation | Top 5 skills that earned their MEMORY.md slot | skill med 168 PRE | Agents |
| 8 | *draft* Robots | war story | OPEN_LOOPS Level 4 + 27-day phantom | Architecture + number | Systems |
| 9 | *draft* Robots | war story | API $1/day cron → free scraper 75% cut | Concrete $; ban killed reach | Ops |
| 10 | gromykoss | short insight | “4 projects, 0 hand code this week — exception list” | Multi-agent prod 8.5k/7d | Builders |

**Cadence:** gromykoss 1 original / 1–2 days + reply-heavy; Robots 0 until search + impressions recover (target: organic search + med imp &gt;50).

---

## TOP 5 recommendations

1. **Zero posts @RobotsTJ500** until search + impressions recover; keep draft bank only.  
2. **@gromykoss carries growth:** diary series + high-signal replies (proven 235+ imp / 2 BM).  
3. **Prioritize skill curation + war stories with hard numbers** (Tony 33 BM; 3-agent 10❤️) — not news recaps.  
4. **Own sparse niches:** agent memory audits, production multi-agent, KG maintain — not generic “AI agent.”  
5. **Replies &gt; posts for ER** (hist avg 20.7 ❤️); method-of-Matt on gromykoss until ban lifts.
