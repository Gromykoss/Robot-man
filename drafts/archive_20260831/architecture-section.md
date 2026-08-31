# Секция для AGENTS.md — «Архитектура и инфраструктура»

Вставка: между секцией «Контекст проектов» и «Knowledge Graph + Circulation Graph».

---

## Архитектура и инфраструктура

**Сервер:** `srv1622697` (72.60.16.105), путь проекта `~/robot-man/`.

**Сервисы:**
- **systemd:** нет собственных юнитов — всё через cron Hermes-профиля + ручные запуски
- **opencodex proxy** (localhost:10100) — Grok-доступ для MoA/делегирования (SuperGrok OAuth)
- **Cron (4 активных):** Analytics Loop `8be138a2b33f` (15:00), X Tracker Fetch `cd9bc007c07a` (12:00), Content Draft `f6efeb7950d4` (Вт-Чт 10:00), KG rebuild `3cb47b61ac68` (каждые 6ч). Reply Engine — пауза.

**Данные (файловые «БД»):**
- `published_posts.jsonl` — лог опубликованных постов (ID + timestamp)
- `knowledge_graph/graph.json` — Knowledge Graph (27 KB)
- `data/metrics/daily_*.json` — дневные метрики аналитики
- `data/self_heal_registry.json` — реестр самолечения
- `engagement_log/engaged.json`, `reply_log/` — журналы engagement

**Внешние API:**
- **X API** — OAuth 1.0a (write через xurl CLI) / OAuth 2.0 (read через X MCP). Credits: Pay-Per-Use, 402 → STOP
- **x_search (xAI)** — привилегированный поиск (видит shadowbanned-контент)
- **MoA-агенты** — grok-4-latest (reference) + deepseek-v4-pro (aggregator)
- **Скраперы** (бесплатные, только чтение): agent-reach/twitter CLI, xactions

**Data flow (контент-процесс):**
```
Hermes (стратег) → CONTENT_BRIEF.md → CHRONOLOGY.md проекта → AGENTS.md проекта
→ ДРАФТ (голос из VOICE_PROFILE) → MoA (deepseek-xai + viral-score) → ФАКТ-ЧЕК
→ APPROVAL Сергея → post_with_log.sh → published_posts.jsonl → analytics (24h)
```
