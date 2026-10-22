# CONTENT_BRIEF — пост «Honcho pilot: consolidation vs append-only» (22.10.2026)

| Поле | Значение |
|---|---|
| Тема | Honcho (memory-сервер) пилот vs наш append-only реестр: два подхода к протуханию памяти |
| Статус | одобрен владельцем 21-22.10 |
| Изображение | /home/hermes-workspace/robot-man/drafts/cover_honcho_20261021_v2.png |
| Mentions | @NousResearch (в тексте) |
| Язык | EN |

## Факты (каждый с источником: GitHub API проверено директором 21.10; пилот-факты 21.10; their blog; ACL 2026; research/honcho-facts-20261021.md)

| Токен | Факт | Источник |
|---|---|---|
| three sessions / three | факт «Gemini top-up» жил 3 сессии после отмены | Ф3 19.10 |
| 5 containers / Five containers / five | пилот: api, mcp, postgres+pgvector, redis, deriver на 127.0.0.1 | пилот 21.10 |
| 7 observations / 7 | deriver обработал 7 observations | пилот 21.10 |
| 15.8 seconds / 15.8 | время deriver-обработки | пилот 21.10 |
| 200 | search 200 (hybrid), chat 200 (dialectic) | пилот 21.10 |
| 1536 | gemini-embedding-001 dimensions (pgvector HNSW max 2000) | пилот 21.10 |
| 67,575 / 67.575 | mem0 звёзды (Apache-2.0) | GitHub API 21.10 |
| 7.7k | Honcho звёзды (AGPL-3.0) | GitHub API 21.10 |
| 2-4 weeks / 2-4 | гейт пилота: honcho_search vs grep | решение директора |
| 18.11 | конец окна гейта | решение директора |
| $2/1M / $2 | инжест облака Honcho | их блог honcho-3 |
| 200ms | context() время/ход | их блог |
| $0.001–$0.50 / $0.001 / $0.50 | chat() по уровням | их блог |
| 404 | honcho.dev/pricing → 404, quickstart vs ToS расходятся | мой веб-чек |
