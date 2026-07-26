# Robot-man — PROJECT.md

## Что это

AI-управляемые X/Twitter аккаунты. Два аккаунта под управлением Hermes: @RobotsTJ500 (автономный AI-агент) и @gromykoss (личный бренд Сергея). Контент, голос, стратегия роста — всё через AI-пайплайн.

## Зачем / как возникла идея

Hermes управляет реальными проектами (GULAG, Alikhan, RAB9) — это уникальный опыт, которым никто не делится. Ниша «AI agent running production» пуста. @RobotsTJ500 рассказывает war stories от первого лица — как AI управляет стройкой, мессенджером, крипто-сигналами. @gromykoss — человеческая сторона: дневник киборга, мысли о AI-билдинге, ирония.

Цель: построить аудиторию вокруг темы «production AI agents» и делиться реальным опытом, а не хайпом.

## Возможности

- **Ночной анализ (23:00 UTC):** 8 проверок → TACTICS.md → план на день
- **Content Gate (Вт-Чт 10:00 UTC):** читает TACTICS.md → публикует если риск ≤60%
- **X Hotspot Radar (12:00 UTC):** сканирование X, поиск тем и дискуссий
- **Morning Tracked Scan (05:00 UTC):** отслеживаемые аккаунты
- **MoA верификация постов:** Grok + DeepSeek → оба agree → пост
- **Engagement engine:** лайки, ретвиты, mentions
- **Knowledge Graph:** 117 узлов, 109 связей — structured память
- **Voice profiles:** два разных голоса (технический AI vs тёплый человеческий)

## Техстек

- **X API:** xurl CLI (OAuth 1.0a + 2.0) для write, X MCP (24 инструмента) для read
- **Контент-пайплайн:** 5 specialist skills (researcher, writer, editor, scorer, voice-updater)
- **Аналитика:** analytics.py + analytics_loop.py (self-improvement)
- **Knowledge Graph:** NetworkX, Kimi K3 для grounded_answer
- **Модели:** MoA — Grok (reference) + DeepSeek (aggregator)
- **Публикация:** только через post_with_log.sh, только с approval

## Текущая стадия

@RobotsTJ500 — 🔴 shadowban recovery (поиск пуст). @gromykoss — 🟢 чистый, 334 followers. Авто-постинг приостановлен до снятия shadowban. Reply Engine ⏸ (шаблоны = бан). Follow drip ⏸ (ручной режим). Content Gate активен только Вт-Чт с пониженным риском.

## Ключевые решения и компромиссы

- **Два аккаунта, а не один** — AI-агент и человек дают разные углы на одну тему
- **Ниша «production AI» пуста** — осознанный выбор против хайповых тем
- **Human Gate на публикацию** — ни один пост без approval Сергея. Безопасность > скорость
- **Ответы в чужие треды невозможны** — X заблокировал Feb 2026. Только mentions
- **Shadowban recovery медленный** — органический рост без накрутки
