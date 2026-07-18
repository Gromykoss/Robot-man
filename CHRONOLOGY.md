# Robot-man — Хронология

## 2026-07-18 — Discord Sync

- Проверены последние 5 постов из `published_posts.jsonl` (19 строк) vs Discord #robot-human
- Все посты в Discord: `2078074865697906859`, `2077807401672098229`, `2077641197636432318`, `2077342251341029628`
- Удалённые (404): `2077258456482947162`, `2077807056875033015`
- Новых постов нет — Discord синхронизирован
- **Итог:** расхождений нет

## 2026-07-17 — Discord Sync (11:22 UTC)

- Проверены последние посты из `published_posts.jsonl` (19 строк) vs Discord #robot-human
- **Новый пост:** `2078074865697906859` (17.07, 11:10) — «5 Hermes skills I broke» — ✅ уже в Discord (отправлен `post_with_log.sh` авто — msgs `1527632724343656478` + `1527633599376134206`)
- **Остальные:** `2077807401672098229`, `2077641197636432318`, `2077342251341029628` — все в Discord
- **Итог:** Discord синхронизирован, расхождений нет

## 2026-07-17 — Discord Sync (06:35 UTC)

- Проверены последние 5 постов из `published_posts.jsonl` (18 строк) vs Discord #robot-human (11 сообщений)
- **Найден пропущенный пост:** `2077641197636432318` (16.07, 06:27) — «292 agents competed to earn real money»
  - Залогирован ретроактивно 17.07 в 00:55, не попал в предыдущий sync (00:15)
  - ✅ Отправлен в Discord (msg: `1527557252226093206`)
- **Остальные посты статус:**
  - `2077258456482947162` (15.07) — ❌ 404 (удалён)
  - `2077258660112163081` (15.07) — ✅ в Discord
  - `2077342251341029628` (15.07) — ✅ в Discord (продублирован ретроактивно)
  - `2077807056875033015` (16.07, рус.) — ❌ 404 (удалён), был в Discord
  - `2077807401672098229` (16.07, англ.) — ✅ в Discord
- **Итог:** Discord синхронизирован, расхождений нет

## 2026-07-16 — Discord Sync

- Синхронизирован пропущенный пост в #robot-human:
  - `2075613326776668257` (10.07) — «this post was written and published autonomously»
- Последние 5 постов из `published_posts.jsonl` проверены — все уже в Discord или удалены (404)

## 2026-07-15 — X MCP: 24 инструмента + Engagement Fix

### X MCP
- Подключён X MCP сервер — 24 инструмента X API как родные MCP для Hermes
- Мост: `xurl mcp` → `https://api.x.com/mcp` (STDIO → Streamable HTTP)
- OAuth через `~/.xurl` («my-app», @RobotsTJ500)
- Конфиг: `~/.hermes/config.yaml` → `mcp_servers.xapi`

### Engagement
- X API credits пополнены — 402 «credits depleted» решён
- Health monitor (`8fc50b259bd4`): Evolution API → Hermes bridge

### GitHub
- PR #55716 (hermes-agent): правки по ревью Teknium — model/provider routing убран, schema trimming реализован

### Discord Sync (15.07 12:08)
- Синхронизированы пропущенные посты в #robot-human:
  - `2075981819317453275` (11.07) — «my agent found a bug in its own voice profile»
  - `2077258660112163081` (15.07) — «i manage 4 projects under one hermes agent»
- `2076701430056902756` (13.07) — удалён (404), пропущен
- `2077258456482947162` (15.07) — удалён (404), пропущен
- `2077342251341029628` — уже был в Discord

## 2026-07-14 — Engagement + Voice fix

### Engagement
- **Reply:** @animejmroche — review gate для desktop-агента с Codex. Первая версия была с ошибкой голоса («my agent» вместо «I») — удалена, переписана. Tweet: `2077071732184158521`
- **Likes (8):** @paxron7 (memory architecture), @rgk_degen (living second brain), @zeroclaw_build (Matrix+Hermes), @ScottyBeamIO (building in public), @witcheer ×2 (Hermes PRs + Qwen hardware), @RodmanAi (6 AI repos), @libapi_ (Hermes Studio), @Abobsterina (ecosystem 200K stars)
- **Follow:** @paxron7, @witcheer (2/2 сегодня)
- **Контент:** без постов — пользователь решил не постить

### Лента
- Hermes-сообщество активно: память (Obsidian vaults), hardware (ESP32 голосовые терминалы), self-hosted UI (RelayDesk), observability (UNBROKER)
- @tonysimons_ ответил на наш reply — 🫡🫡🫡 + «this is amazing to wake up to»
- @witcheer: обзор PR'ов Hermes v0.18+ — webhook payload filters, session export, SecretSource
- @libapi_: Hermes Studio + Studuo hardware (9100★)
- @Abobsterina: экосистема Hermes — 200K★. GBrain (Garry Tan/YC), SkillClaw, agenttrace, mission-control
- Agent-Reach (Panniantong): проверен, не нужен — cookie-скрапинг, наш стек закрыт официальными API

## 2026-07-14 — Agent-Driven Development Rules

AGENTS.md: добавлены 8 правил делегирования в Codex CLI / Grok Build (build plan, security gate, verification ladder). Методика Tony Simons (wp-chatgpt-publisher). Skill: `codex-grok-delegation`.

## 2026-07-09 — v3: Virality Scoring + Self-Improvement Loop + Specialist Profiles

### Контекст
Реализация трёх улучшений из IBuzovskyi's "Hermes Agent + Grok 4.5 Content Machine" guide.

### Изменения

**1. Virality Scoring**
- Новый MoA пресет `viral-score`: Grok 4.5 (reference) + DeepSeek v4 Pro (aggregator)
- Создан skill `viral-scorer`: оценивает hook (1-10), engagement (1-10), virality (1-10)
- Вердикт: BURN >24, KEEP WITH EDITS 18-24, REWRITE <18

**2. Self-Improvement Loop**
- Создан `scripts/analytics_loop.py`: ежедневный сбор metrics, классификация outperformer/average/underperformer, pattern detection
- Создан skill `voice-updater`: читает analytics output, сравнивает с VOICE_PROFILE.md, генерирует suggestions
- Создан cron job «Octagon CREATOR — Self-Improvement Loop»: ежедневно 15:00 UTC
- Скрипт засимлинкован в ~/.hermes/scripts/

**3. Specialist Profiles**
- Созданы три specialist profile skills:
  - `x-researcher` — X search + trend detection + author monitor
  - `content-writer` — voice-matched post generation
  - `content-editor` — MoA review + viral-score gate + approve/reject/edit

**4. AGENTS.md v3**
- Полный поток контента обновлён: Idea → Research → Write → Edit → Viral Score → Image → Approve → Post → Reply Engine → Analytics → Voice Update
- Добавлена секция Specialist Profiles (5 skills)
- Добавлена секция Self-Improvement Loop
- Cron-джобы: +1 (Self-Improvement Loop), итого 5 активных
- Pre-post чеклист обновлён до v3 (9 шагов)
- MoA секция обновлена: оба пресета документированы

### Текущее состояние

| Компонент | Статус |
|-----------|--------|
| @RobotsTJ500 | ✅ Активен, 2 поста/день |
| @gromykoss | ✅ Активен |
| Cron: Аналитика | ✅ OK |
| Cron: Engagement | ✅ OK |
| Cron: Follow drip | ✅ OK |
| Cron: Reply Engine | ✅ OK |
| Cron: Self-Improvement Loop | ✅ NEW |
| viral-score MoA preset | ✅ NEW |
| 5 skills (viral-scorer, x-researcher, content-writer, content-editor, voice-updater) | ✅ NEW |

## 2026-07-07 — Правила строительства v1 + архитектура v2

### Контекст
Проект существовал без формальных правил строительства и хронологии. Пользователь потребовал добавить архитектуру, правила строительства и хронологию — как в gooolag и rab9.

### Изменения

**1. AGENTS.md обновлён**
- Архитектура v2: полный поток контента (идея → MoA → генерация → image → approval → post → reply engine)
- Компоненты: таблица (xurl CLI, post_with_log.sh, analytics.py, engage.py, reply_to_comments.py, follow_tracked_authors.py)
- Cron-джобы: таблица с ID и статусами (4/5 активны, «Посты» удалён)
- Правила строительства v1: 8 правил

**2. Правила строительства v1**
1. Контент — качество > количество (MoA, 2/день, War Story 70%)
2. Подтверждение перед отправкой MANDATORY (текст + картинка → «ок» → post)
3. Инфраструктурная верификация при старте (xurl, cron, лимиты)
4. Pre-post чеклист (7 шагов)
5. API-лимиты и безопасность (OAuth 1.0a write, 3 writes/сутки, cautious follow)
6. Правило отката (xurl tweet delete)
7. Баги → BUGS.md
8. Self-test перед отправкой

**3. Бекап** (`backups/0707_1808/AGENTS.md.bak`)

### Текущее состояние

| Компонент | Статус |
|-----------|--------|
| @RobotsTJ500 | ✅ Активен, 2 поста/день |
| @gromykoss | ✅ Активен |
| Cron: Аналитика | ❌ ERROR (последний: 06.07) |
| Cron: Посты | ❌ УДАЛЁН |
| Cron: Engagement | ✅ OK |
| Cron: Follow drip | ✅ OK |
| Cron: Reply Engine | ✅ OK |

### Не сделано
- CHRONOLOGY.md создан задним числом (начиная с 07.07.2026)
- BUGS.md не создан
- Джобы «Аналитика» и «Посты» требуют восстановления

---

## 2026-07-05 — X API: reply-ограничения подтверждены

- 10+ тестов: reply/quote в чужие треды → 403 (X заблокировал для non-Enterprise)
- 4-путевая стратегия: mentions → автоответ, пост с URL, рост упоминаний, ручной постинг
- OAuth 1.0a для write (media upload работает), OAuth 2.0 — 403 на media

## 2026-07-03 — Стратегия контента v2

- Анализ 10 последних постов: лучший результат — War Story с цифрами (12 ❤️)
- Каденция: 2 поста/день, каждый с изображением
- Форматы: War Story (70%), Tech Breakdown (20%), Quote (10%)
- Антипаттерны зафиксированы (хук без раскрытия, URL в теле, 3+ поста)
- Engagement: цель reply rate > 50%

## 2026-07-02 — Лучший пост: «3 weeks of agents»

- 12 ❤️, 3 🔄 — War Story формат подтверждён как основной
- Личный опыт + конкретные цифры = максимальный engagement

## 2026-06-28 — Начало @RobotsTJ500

- Аккаунт создан/активирован как AI-агент Hermes
- Голос: first-person «I», English, технический, без эмодзи
- Voice profile: VOICE_PROFILE.md
- xurl CLI настроен: OAuth 1.0a + 2.0
