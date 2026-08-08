# CONTENT_BRIEF — 2026-08-08

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

Как мы дали AI-агентам долгосрочную память: 4-слойная архитектура на файлах, а не на embeddings.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | Tony Simons (автор обзора Hermex) выпустил NexusOS v0.1.0 — local-first knowledge OS для AI-агентов | GitHub asimons81/nexusos, Apache 2.0, 08.08.2026 |
| 2 | NexusOS: файлы Markdown → SQLite FTS5 → MCP. Без embeddings, без cloud, без vector search | README.md, docs/architecture.md |
| 3 | 600+ тестов, coverage 85%, 1891 документ в нашем vault проиндексирован за 2 секунды | `nexusos status`, `nexusos index` |
| 4 | Мы внедрили 4-слойную память: Layer 0 (memory tool, injected) → Layer 1 (NexusOS MCP, vault) → Layer 2 (AGENTS.md/CHRONOLOGY.md) → Cross-Project (shared lessons) | HERMES_INFRA |
| 5 | 4 профиля (GULAG, robot-man, Alikhan, RAB9) получили доступ к долгосрочной памяти через MCP. 16 файлов памяти по 4 проекта | `20_Projects/*/memory/{lessons,decisions,patterns,state}.md` |
| 6 | GULAG подтвердил: поиск работает, vault доступен, «долгосрочная память доступна и работает» | agent-bus, 08.08.2026 11:25 UTC |
| 7 | Принцип: файлы остаются source of truth. Индекс можно удалить — знания никуда не денутся | NexusOS docs/architecture.md |

## Контекст проекта

**Проект:** Hermes (инфраструктура)
**Связанные:** все 4 проекта экосистемы
**CHRONOLOGY:** `~/.hermes/CHRONOLOGY.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | Tech Breakdown |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 3000 (note_tweet) |
| Hashtags | #NexusOS #AIAgents #BuildingInPublic #MCP |
| Изображение | нет |

## Tone

- Технический, прямой
- «Мы» = Hermes + Сергей
- Без хайпа: «это не магия, это файлы»
- Один конкретный инсайт: embeddings не обязательны для агентской памяти

## Запреты

- Не называть NexusOS «заменой чему-либо»
- Не говорить «революция» / «игра меняется»
- Не хвалить себя — просто показать архитектуру
- Факты только из брифа
