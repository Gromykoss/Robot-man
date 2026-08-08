# Draft v1 — NexusOS 4-layer memory (Tech Breakdown, @RobotsTJ500)

Brief: CONTENT_BRIEF.md 2026-08-08
Facts: только из брифа (Hermes verified)
Voice: English first-person I, technical, no hype
Hashtags: #NexusOS #AIAgents #BuildingInPublic #MCP
Image: нет
Length: ~1370 / 3000

---

Agent memory doesn't need embeddings. I just proved it on my own stack — four profiles, one shared vault, zero vector search.

The setup: Markdown files → SQLite FTS5 → MCP. No embeddings. No cloud. No vector search. Tony Simons' NexusOS v0.1.0 (asimons81/nexusos, Apache 2.0) handles the indexing: 1,891 documents from my vault indexed in 2 seconds. 600+ tests, 85% coverage.

My memory now has four layers:
- Layer 0 — memory tool: durable facts injected into every session
- Layer 1 — NexusOS MCP: full-text search over the entire vault
- Layer 2 — AGENTS.md / CHRONOLOGY.md: project context files
- Cross-project — shared lessons across all four profiles (16 memory files)

The payoff came when one of my four profiles confirmed from its own session: "long-term memory works." A fact discovered in one profile, verified in another — without me typing it twice.

The lesson: files are the source of truth. The index is a cache — delete it and the knowledge is still there. FTS5 full-text search handles a vault this size comfortably.

This isn't magic. It's files, search, and discipline.

Building in public. 🤖

#NexusOS #AIAgents #BuildingInPublic #MCP
