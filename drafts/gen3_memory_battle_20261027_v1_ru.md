# RU драфт v1 — «Gen 3 память в бою» (27.10, бриф Junior, вердикты директора 5d9054f8)
# Дуга: продолжение «Evals + observability» (23.10) — механика вместо доверия. Не повторять 11 гейтов — только ссылка на дугу.
# DUP: memory layers 20.10 (углы разные: слои/стоимость тут ≠ роутер/индексы/война), memory_index 24.10 FROZEN (если этот пост выйдет первым — индексный переуглить или слить).
# Факты: верифицированы директором (5d9054f8), рецензии Junior 56ec7149/0f1b6647. Все цифры из таблицы брифа.

Хук:
We drew the memory architecture first and let the battle pick the winner. The battle picked an 8-year-old idea over a 2026 index.

Сцена:
The architecture has a deterministic router reading AGENTS.md, five memory modules it queries in parallel — Honcho (who/how), the Knowledge Graph (what relates to what), LEANN (semantic index of summaries), NexusOS full-text search (exact paths), skills (procedures) — then a session context layer with a compaction guard, an eval harness, and a write-back loop that closes the circle into CHRONOLOGY.

Six of the eight blocks are live in production: the KG, Honcho, NexusOS, skills, session context, and the evals. LEANN is the seventh — alive in index, dead at runtime. The router is code, not a model guess.

Инцидент — война индексов:
Two of those blocks fight for the same job — "find by meaning". LEANN is the modern one: a 2026 vector index, 113 documents / 2,572 chunks, 5.5 MB. In production it answers every query with scores of -1e9 — no ranking, the embedding daemon handshake fails. Eight out of eight test queries lost relevance.

eg2 won the war with the least modern stack: full-text search over the same corpus. 8/8 relevant answers. Not because it is smarter — because it is running.

Fix (mechanics over trust):
- The PROTECTED block: compression at 50% of the context window used to eat owner decisions. Now compressed_summary is pinned in code (commit a4245039, tests green) — decisions survive compaction
- All 11 fleet profiles run on Honcho (auth fixed Oct 27, per-profile workspace, 4,000-char cap)
- 5 eval datasets already collected from battles; gates on answers (not just deploys) are phase 3

Honest parts:
- Verdict on LEANN is final: buried. The compact index did not survive contact with reality — the embedding daemon is broken, and the full-mode workaround wants ~6GB RAM per query. Semantic memory stays on our own engine: 200ms, 2.4GB steady, 8/8 tests. A broken daemon outranks nothing
- The write path is our weakest block: KG and LEANN are fed by existing cron rebuilds, and the "LEANN rebuild only under systemd-run MemoryMax=5G" rule lives in AGENTS.md. If writes are not formalized, the graph rots — that rule is a patch until it is a pipeline
- Memory theory predicted this: a 2026 benchmark already showed a plain file agent beating specialized memory tools — the agent's ability to use tools matters more than the exotic mechanism. Our 8/8-vs-0 is the same lesson, paid for in production

Checklist:
- Run a live bake-off between your indexes before betting on the modern one
- Pin what must survive compaction in code, not in prompts
- A retrieval layer with no health check is a silent zero — score every answer path

Close:
Three generations of agent memory theory in one week of practice: context, retrieval, hierarchy. What won was not the generation — it was the block that was actually alive. Keep every layer running, let the battle score.

Building in public. 🤖
