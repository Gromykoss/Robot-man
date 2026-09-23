# robot-man BUGS.md — Known Issues & Technical Debt

_No known bugs at this time._

---

This file serves as a living registry of known issues. Add entries as bugs are discovered during development, testing, or production monitoring.

### Template for new entries:

```
### N. Bug Title
**Severity:** Low / Medium / High / Critical
**Status:** 🔴 Active / ⏳ Investigating / 📅 Scheduled / ✅ Resolved
**Details:** Description of the issue, reproduction steps (if known), and any mitigation workarounds.
```

### 1. analytics_loop.py ACCOUNT_ID указывает на dataPort_agent, не на @RobotsTJ500
**Severity:** Medium
**Status:** 📅 Scheduled
**Details:** Константа ACCOUNT_ID=1871454196295479296 в scripts/analytics_loop.py принадлежит @dataPort_agent (name "DataPort Navigator"), а не @RobotsTJ500. Реальный id @RobotsTJ500 = 1880157852632772608 (проверено через /2/users/by/username 2026-09-07). Влияние ограничено: основные метрики скрипт берёт из published_posts.jsonl и по username Gromykoss, ACCOUNT_ID сейчас не используется в расчётах отчёта. Fix требует approval (код проекта — зона Codex).

| 23.09.2026 | BUG-ANALYTICS-DUP | analytics_loop учитывает один пост ×4 (дубли 21007159/21007161 в отчёте), self-reply 'Failed to fetch' | дедупликация по tweet id при агрегации; self-reply фильтр | ОТКРЫТ |
| 23.09.2026 | BUG-XACTIONS-DEAD | xactions search/trends пустые всю ночь (4+ запроса) | замена на X MCP x_search до починки | ОТКРЫТ |
| 23.09.2026 | BUG-DELETE-SYNTAX | 'xurl tweet delete ID' возвращал {} но твит оставался жив; рабочий синтаксис: 'xurl delete ID' | использовать 'xurl delete'; после удаления всегда read-back | ЗАКРЫТ |
