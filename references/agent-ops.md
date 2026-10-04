# References — тактика и operational details (robot-man)

Вынесено из AGENTS.md при редакции 04.10 (аудит MGT_maccha п.3, приказ оператора).
Инварианты (gates, Human Gate, публикация-путь, anti-ban) остались в AGENTS.md.

## Cron-джобы — снапшот 04.10.2026 (аудит MGT_maccha 02.10)

Источник истины: `~/.hermes/profiles/robot-man/cron/jobs.json` (и `~/.hermes/cron/jobs.json` для default).

| Джоб | ID | Расписание | Что делает |
|------|-----|-----------|------------|
| ~~Analytics Loop~~ | ~~`8be138a2b33f`~~ | — | ❌ УДАЛЁН: джоба не существует ни в одном профиле (проверено 23.09, cronjob list) |
| X Tracker Fetch | `cd9bc007c07a` | 0 12 * * * | Посты отслеживаемых аккаунтов (джоба живёт, прогоны ok 04.10; ⚠️ cookie-сессия сдохла, данных нет с 18.09; реавторизация — у оператора) |
| KG rebuild | `4506b578cfa3` (default) | 0 0,6,12,18 * * * | Knowledge Graph перестроение (действующий; прогон 04.10 12:00 ok). ⚠️ ff5f0025c0e7 — это KG Alikhan, сюда не входит |
| ~~KG rebuild~~ | ~~`3cb47b61ac68`~~ | — | ❌ Застыла 05.09 при `0 */6 * * *`; решение оператора (dup default) |
| Утренняя тактика TACTICS.md | `1abd8129a7d4` | 0 5 * * * | Генерация TACTICS.md, антидубль по published_topic_check.py |
| ~~Тактика @gromykoss~~ | ~~`79135324410a`~~ | — | ⏸ ПАУЗА 22.09: gromykoss вне пайплайна (директива владельца) |
| ~~KSimback reply watchdog~~ | ~~`de5bfff310c8`~~ | — | ❌ Пауза 05.09: state stale 17d, thread dead |
| CHRONOLOGY + брифинг | `b130f291b70a` | 45 22 * * * | CHRONOLOGY.md + daily-брифинг в briefings/ |
| catmanyau dialog watchdog | `aa467847d5e2` | every 240m | Мониторинг диалога @catmanyau, агент-обёртка только на DIALOG_UPDATE |
| jev-learner | `92f23779bd70` | 30 9 * * * | VOICE_LESSONS.md из пар драфт→финал (no-agent, resume-safe) |
| jev-analyzer | `2a7b273874df` | 0 12 * * 0 | Свежий 7-дневный корпус + Jev-скоринг + отчёт (no-agent) |
| Robot-man weekly analytics | `87832edf5bc3` (default) | 0 10 * * 1 | Еженедельная аналитика (ok 28.09) |

- Одноразовые completed-джобы (e51ec23ca64f, 9c2ab06dd560, 8d639cdeaa03, 46168f4fbe70) не включены — выполнились, архив в jobs.json.
- **Статус:** Reply Engine ⏸ пауза (шаблоны = бан). ~~Shadowban-чекер `828224497fc3`~~ — ❌ ВЫЧЕРКНУТ (оператор 25.09).
- Jev-скрипты: `scripts/jev_corpus_collector.py` + wrappers `~/.hermes/profiles/robot-man/scripts/jev_{learner,analyzer}.sh`.

## Инфраструктура

- **Сервер:** VPS Hostinger 72.60.16.105 (общий хост Hermes), Ubuntu 24.04, 15 GB RAM.
- **БД:** Knowledge Graph — `knowledge_graph/graph.json` + `scripts/knowledge_graph.py`.
- **Внешние API:** xurl CLI (OAuth 1.0a — write), X MCP/xurl bridge (OAuth 2.0 — read), xactions MCP (scraping read-only), agent-reach + twitter CLI (бесплатный scraping), xAI Aurora (изображения). **x-monitor — ⛔ DEPRECATED.**
- **TTS:** voice-matching / TTS — генерация аудио.

## X API: возможности и ограничения

| Операция | Статус |
|----------|--------|
| Читать посты, search, mentions | ✅ OAuth 1.0a/2.0 |
| Постить текст/медиа, Reply (свои + mentions), Like/Repost/Follow, DM | ✅ OAuth 1.0a |
| Reply чужим / Quote | ❌ X блок Feb 2026 |

**Длинные посты (Premium, 4000 символов):** полный текст в `note_tweet.text`. Всегда запрашивать `tweet.fields=note_tweet`:
`xurl --app my-app --auth oauth2 -u '@user' "/2/tweets/ID?tweet.fields=note_tweet"` / `xurl post --app my-app --auth oauth2 -u '@user' "текст до 4000"`

**Откат:** `xurl --app my-app --auth oauth1 -u RobotsTJ500 tweet delete POST_ID`. Не злоупотреблять.

## Стратегия реплаев (4 пути)

1. Mentions (`xurl mentions`) · 2. Пост с URL · 3. Рост упоминаний · 4. Подготовка текста → Сергей постит вручную.

## Self-test перед отправкой

BRIEF / КОНТЕКСТ / ГРАФ / WRITE / MoA / ФАКТ-ЧЕК / Изображение / Формат / note_tweet / 24h analytics.

## MoA пресеты (v3)

| Пресет | Reference | Aggregator | Когда |
|--------|-----------|------------|-------|
| `deepseek-xai` | grok-4-latest | deepseek-v4-pro | Hook + voice |
| `viral-score` | grok-4-latest | deepseek-v4-pro | Hook/engagement/virality (1-10) |

Оба agree → пост. Иначе — переписать.

## Verification ladder (Agent-Driven Development)

`xurl auth status` → MoA → vision_analyze → cronjob list → Сергей → post_with_log.sh → CHRONOLOGY.md.

## Верификация при старте

X MCP tools (`get_users_me`), `cronjob list` (фильтр robot-man), `cat published_posts.jsonl | tail -3`, API лимиты.

## Файлы проекта

| Файл | Для чего |
|------|----------|
| `AGENTS.md` | Канон отдела (инварианты) |
| `CONTENT_BRIEF_TEMPLATE.md` | Шаблон брифинга от Hermes |
| `STRATEGY.md` | Стратегия (канон, зона Hermes) |
| `VOICE_PROFILE.md` / `VOICE_PROFILE_GROMYKOSS.md` | Голоса аккаунтов |
| `analytics.py` / `scripts/analytics_loop.py` | Аналитика + self-improvement |
| `engage.py` / `mutuals_follow_back.py` / `follow_tracked_authors.py` | Engagement |
| `post_with_log.sh` | Публикация + лог (единственный путь) |
| `published_posts.jsonl` | Лог опубликованных постов |
| `skills/*/SKILL.md` | Specialist skills |
