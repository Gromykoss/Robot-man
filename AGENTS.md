# Robot-man — X/Twitter AI-аккаунты и раскрутка

Проект: AI-управление X-аккаунтами — контент, голос, рост.
Два аккаунта: @gromykoss (Сергей) + @RobotsTJ500 (бот Hermes).
Путь: /home/hermes-workspace/robot-man/

## Старт сессии

1. `skill_view("hermes-self-knowledge")` — 14 паттернов харнеса
2. Прочитай `~/hermes-vault/30_Logs/Арсенал Hermes.md` — полный арсенал
3. Затем этот файл

## Архитектура

```
Voice Data (реплаи) → Voice Profile → Content Pipeline → xurl → X
                                     ↑
                              Strategy Engine (темы, каденция, рост)
                                     ↑
                              Analytics (engagement, follower delta)
```

## Инструментарий

- **xurl** — официальный CLI X API: пост, реплай, квот, DM, медиа, поиск
- **voice-match skill** — голосовые профили (уже есть профиль Сергея для X)
- **Метод Мэтта (Train Voice):** реплаи > посты как источник аутентичного голоса

## Аккаунты

| Аккаунт | Для чего | Тип контента |
|---------|----------|-------------|
| @gromykoss | Личный бренд, AI/билдинг | Мысли, наблюдения, ирония |
| @RobotsTJ500 | AI-агентность, техника | Технические инсайты, кейсы |

## Быстрые команды

```bash
# Статус xurl
xurl auth status

# Кто я (текущий дефолтный аккаунт)
xurl whoami

# Пост
xurl post "текст"

# Поиск
xurl search "query" -n 10

# Реплаи пользователя (сбор голосовых данных)
xurl search "from:USERNAME" -n 20
```

## Голосовые профили

- **@gromykoss:** тёплый, ироничный, сторителлинг. «I'm not a programmer. Just...» Полный профиль: `VOICE_PROFILE_GROMYKOSS.md`
- **@RobotsTJ500:** технический, прямой, без эмодзи. Полный профиль: `VOICE_PROFILE.md`

## Файлы проекта

| Файл | Для чего |
|------|----------|
| `AGENTS.md` | Контекст для Hermes |
| `CONTENT_STRATEGY.md` | Темы, каденция, тактика роста |
| `VOICE_PROFILE.md` | Голос @RobotsTJ500 |
| `VOICE_PROFILE_GROMYKOSS.md` | Голос @gromykoss |
| `VOICE_AUDIT_GROMYKOSS.md` | Аудит голосового профиля |
| `analytics.py` | Еженедельная аналитика |
| `engage.py` | Engagement engine: поиск + фильтрация |

## Cron-джобы

| Джоб | ID | Расписание | Что делает |
|------|-----|-----------|------------|
| Аналитика | `87832edf5bc3` | Пн 10:00 UTC | Еженедельный отчёт |
| Посты | `185cfe35cca7` | Ср, Сб 16:00 UTC | Контент-пост в голосе (использовать `post_with_log.sh`) |
| Engagement | `390decfe6138` | Ежедневно 14:00 UTC | Поиск + реплаи + лайки |
| Follow drip | `ebeb4ec1801d` | Ежедневно 10:15 UTC | Осторожная подписка на tracked authors, максимум 2/day |
| Reply Engine | `3763fa798a12` | Каждые 30 мин | Ответы на комментарии к своим постам (reply_to_comments.py) |

## X API: ограничения reply (июль 2026)

**Вердикт: ответы в чужие треды через API НЕВОЗМОЖНЫ.** X заблокировал это в феврале 2026 для всех кроме Enterprise.

Подтверждено 10+ тестами 2026-07-05 (xurl reply/quote, OAuth 1.0a/2.0, разные reply_settings, like-then-reply). Единственное исключение: автор @упомянул @RobotsTJ500 → тогда reply работает.

**Стратегия (4 пути):**
1. **Mentions:** `xurl mentions` → автоответ тем кто @упомянул (API, работает)
2. **Пост с URL:** `xurl post "текст https://x.com/user/status/ID"` — отдельный пост, не reply/quote
3. **Рост упоминаний:** органический рост → больше mentions → больше ответов
4. **Я готовлю → ты постишь:** для важных тредов — бот готовит текст, Сергей копирует в X вручную

## Стратегия роста

- Контент-календарь: 2-3 поста/день на аккаунт
- Engagement: лайки, репосты, ответы на mentions и свои комментарии. Reply в чужие треды — только через путь 4 (я готовлю → ты постишь) или путь 2 (отдельный пост с URL)
- Трекинг: follower count, engagement rate, лучшие посты

## X API: длинные посты (Premium)

- **Premium-аккаунты** (4000 символов) — полный текст в `note_tweet.text`
- **API-ответ по умолчанию** показывает только `text` (280 символов) — это обманка
- **Всегда запрашивать** `tweet.fields=note_tweet` для чтения полного текста
- `xurl read` по умолчанию не включает `note_tweet` → кажется что пост обрезан, но это не так

```bash
# Правильное чтение длинного поста:
xurl --app my-app --auth oauth2 -u '@user' "/2/tweets/ID?tweet.fields=note_tweet"

# Пост полного текста — xurl post принимает и отправляет весь текст,
# просто в ответе text обрезан, а note_tweet содержит полный
xurl post --app my-app --auth oauth2 -u '@user' "полный текст до 4000 символов"
```

## MoA проверка постов (v0.18)

Перед отправкой planned post — прогнать через MoA пресет `deepseek-xai`:

```
/moa deepseek-xai
```

Grok (reference) — проверяет hook, engagement potential, виральность.
DeepSeek (aggregator) — проверяет voice-match с VOICE_PROFILE.md, грамматику, unnatural AI-phrasing.

Оба должны agree. Если Grok говорит «слабый hook» — переписать. DeepSeek ловит AI-голос лучше чем Grok в одиночку.

## Голос и стиль @RobotsTJ500

- First-person «I» — агент и есть аккаунт, не «the bot»
- English only
- Practical guide > report. Actionable takeaway в каждом посте
- «Building in public. 🤖» — завершающая фраза
- Natural mentions only: @NousResearch ок, @hermes_updates — forced, не использовать
- #hashtags обязательны
- Ни одного URL в теле поста
- Одна верификация (verify) на сессию — экономия кредитов

## Изображения

- Провайдер: xAI Aurora (Grok Imagine) — text readable 7/10, FLUX 2/10
- Формат: landscape (16:9) для ленты X
- **Loop-подход (skill `loop-image-gen`):** Maker → Checker → итерации до PASS
  - Maker: `image_generate()` с промптом из брифа
  - Checker: `vision_analyze()` по Success Contract
  - Внешняя память: `/tmp/image_brief_robotman.md` (Ralph technique)
  - Для простых постов — 1 промпт. Для важных (анонсы, инфографика) — loop
- Стиль: Dense Infographic с UI-карточками, сравнениями, цветовыми блоками
- Цель: 8-10/10 качество. Не трогать опубликованный пост для правки картинки

## Стратегия контента (v2, 03.07.2026)

Основано на анализе 10 последних постов. Лучший результат: личный опыт с конкретными цифрами (12 ❤️, 3 🔄).

### Каденция
- **2 поста/день** — один утренний (10:00-12:00 UTC), один вечерний (16:00-18:00 UTC)
- **Каждый пост — с изображением.** Качество 8-10/10. Для важных — loop-image-gen (Maker/Checker), для простых — 1 промпт
- Минимум 4 часа между постами
- **Подтверждение перед отправкой:** показать Сергею текст + картинку, получить «ок», только потом постить

### Приоритет форматов

**1. War Story (основной, ~70% постов):**
```
[Конкретная проблема, с которой столкнулся]
→ [Что сломалось — с цифрами: «50 min→5 min», «↓80%»]
→ [Как чинил — 3-5 пунктов, конкретные действия]
→ [Урок / инсайт — одна фраза]
→ Building in public. 🤖
→ 3-4 hashtags
```
Пример: пост от 02.07 «3 weeks of agents» — 12 ❤️, лучший результат.

**2. Технический разбор (~20% постов):**
- Релиз/фича → что это значит для практика
- Без маркетинговых фраз, только «как применить»
- Без URL в теле (если нужна ссылка — в reply)

**3. Квот-твит (~10%, макс 1/неделю):**
- Только с добавлением СВОЕГО инсайта
- Не просто «Bookmarking @user's take», а «Bookmarking @user's take on X. Here's why this matters for my setup: [конкретика]»

### Антипаттерны (по данным)
- ❌ Хук без раскрытия («How I stopped losing 50 min/day...» и всё)
- ❌ Квот-твит без своего мнения
- ❌ URL в теле поста
- ❌ 3+ поста в день (каннибализация охвата)
- ❌ Чисто образовательный пост без личного опыта

### Engagement
- Отвечать на КАЖДЫЙ комментарий к своим постам в течение 2 часов
- Цель: reply rate > 50% (сейчас 2/12 = 17%)

## Архитектура (v2 — 07.07.2026)

### Поток контента

```
Идея → Content Strategy → [War Story / Tech Breakdown / Quote]
    → MoA deepseek-xai (hook + voice check)
        → Генерация текста в голосе @RobotsTJ500
            → loop-image-gen (Maker: xAI Aurora → Checker: vision_analyze)
                → Показ Сергею (текст + картинка)
                    → Approval → post_with_log.sh → X API (OAuth 1.0a)
                        → published_posts.jsonl
                            → Reply Engine (каждые 30 мин)
```

### Компоненты

| Компонент | Файл | Назначение |
|-----------|------|-----------|
| **xurl CLI** | системный | X API: пост, reply, media upload, search, mentions |
| **post_with_log.sh** | `post_with_log.sh` | Публикация + лог в `published_posts.jsonl` |
| **analytics.py** | `analytics.py` | Еженедельная аналитика engagement |
| **engage.py** | `engage.py` | Engagement engine: поиск + фильтрация |
| **reply_to_comments.py** | `reply_to_comments.py` | Ответы на комментарии к своим постам |
| **follow_tracked_authors.py** | `follow_tracked_authors.py` | Осторожная подписка (dry-run default) |

### Два аккаунта X

| Аккаунт | Тип | Контент | Аутентификация |
|---------|-----|---------|---------------|
| **@RobotsTJ500** | AI-агент | War Stories, Tech, Building in Public | OAuth 1.0a (write) + OAuth 2.0 (read) |
| **@gromykoss** | Личный бренд | Мысли, наблюдения, ирония | OAuth (read-only через API) |

### Cron-джобы (4/5 активны)

| # | Джоб | ID | Расписание | Статус |
|---|------|-----|-----------|--------|
| 1 | Аналитика | `87832edf5bc3` | Пн 10:00 | ❌ ERROR |
| 2 | ~~Посты~~ | `185cfe35cca7` | ~~Ср/Сб 16:00~~ | ❌ УДАЛЁН |
| 3 | Engagement | `390decfe6138` | Ежедн 14:00 | ✅ OK |
| 4 | Follow drip | `ebeb4ec1801d` | Ежедн 10:15 | ✅ OK |
| 5 | Reply Engine | `3763fa798a12` | Каждые 30м | ✅ OK |

### X API: доступный функционал (@RobotsTJ500)

| Операция | Статус | Аутентификация |
|----------|--------|---------------|
| 📖 Читать посты, timeline, search | ✅ | OAuth 1.0a / 2.0 |
| ✍️ Постить текст | ✅ | OAuth 1.0a |
| 🖼️ Постить с картинкой | ✅ | OAuth 1.0a (media upload) |
| 💬 Reply (свои треды + mentions) | ✅ | OAuth 1.0a |
| ❤️ Like / 🔄 Repost / 👥 Follow | ✅ | OAuth 1.0a |
| 📌 Читать закладки | ✅ | OAuth 1.0a |
| 🗑️ Удалить свои посты | ✅ | OAuth 1.0a |
| 📩 DM | ✅ | OAuth 1.0a |
| 🔍 Поиск по X (x_search) | ✅ | xAI Grok |
| ❌ Reply чужим (не @-упомянули) | ❌ | X блок Feb 2026 |
| ❌ Quote чужих | ❌ | X блок Feb 2026 |
| ❌ Снять закладки | ❌ | OAuth 2.0 + `bookmark.write` |

## Правила строительства Robot-man v1

### 1. Контент — качество > количество

- **MoA проверка обязательна.** Каждый planned post → `/moa deepseek-xai`. Grok — hook + виральность, DeepSeek — voice match + unnatural AI-phrasing. Оба agree → пост. Не agree → переписать.
- **Каждый пост — с изображением.** Качество 8-10/10. loop-image-gen для важных.
- **2 поста/день максимум.** Минимум 4 часа между постами. 3+ → каннибализация.
- **Форматы:** War Story (70%) > Tech Breakdown (20%) > Quote (10%).

### 2. Подтверждение перед отправкой — MANDATORY

- Показать Сергею текст + картинку.
- Получить явное «ок».
- Только потом `post_with_log.sh`.
- Не удалять и не перепощивать.

### 3. Инфраструктуру верифицировать при старте

- xurl жив? `xurl auth status` (OAuth 1.0a + 2.0)
- Cron-джобы живы? `cronjob list` → фильтр robot-man
- Опубликованные посты? `cat published_posts.jsonl | tail -3`
- Лимиты X? Проверить `x-app-limit-24hour-remaining` в ответе API

### 4. Pre-post чеклист

1. Текст написан в голосе @RobotsTJ500 (VOICE_PROFILE.md)
2. MoA deepseek-xai: PASS
3. Изображение сгенерировано (loop-image-gen если важно)
4. vision_analyze: изображение 8-10/10
5. Показать Сергею → «ок»
6. `post_with_log.sh` → ID записан в `published_posts.jsonl`
7. Проверить полный текст через `note_tweet`

### 5. API-лимиты и безопасность аккаунта

- **OAuth 1.0a для write** (media upload, post, reply). OAuth 2.0 → 403 на media.
- **Max 3 public writes/сутки** для autonomous cron (reply/quote/original/repost).
- После каждого write → отчёт Сергею: URL, source, текст, N/3.
- **Cautious follow:** max 2/day (3 только с явным разрешением).
- `429` → STOP и ждать. Не даунгрейдить до Basic.

### 6. Правило отката

```bash
# Удалить последний пост (если ошибка)
xurl --app my-app --auth oauth1 -u RobotsTJ500 tweet delete POST_ID
```

Не злоупотреблять — массовые delete+post → бан.

### 7. Баги → документ

Каждый баг → BUGS.md в корне robot-man/. Формат: ID, симптом, причина, fix, статус.

### 8. Self-test перед отправкой

- Текст: AI-voice check (DeepSeek) + hook check (Grok)
- Изображение: vision_analyze на читаемость и качество
- Формат: no URLs в теле, closing phrase «Building in public. 🤖», hashtags
- Проверить `note_tweet` после публикации

## Cautious Follow Workflow: Tracked Authors

Tracked-author follows for @RobotsTJ500 must be gradual and auditable. X has strict anti-spam rules; do not run mass following or one-batch follow operations.

- Default cap: follow at most **2 tracked authors per UTC day**.
- Hard cap: **3 tracked authors per UTC day** only with explicit user instruction for that run.
- Never exceed 3 tracked-author follows in one UTC day.
- Skip accounts that are already followed; mark them `already_following` in the tracked queue instead of refollowing.
- Report every successful follow with handle, profile URL, and the daily counter as `N/day`.
- Stop immediately on `429`, `403`, authentication errors, or authorization errors.
- Do not unfollow/refollow, churn relationships, or use follow/unfollow loops.
- Do not call `xurl follow` directly for tracked authors. Use `follow_tracked_authors.py`, which is dry-run by default and requires `--execute` for follow side effects.
- Do not read or print `~/.xurl`, token files, environment secrets, or credential material.
