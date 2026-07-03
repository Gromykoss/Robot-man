# Robot-man — X/Twitter AI-аккаунты и раскрутка

Проект: AI-управление X-аккаунтами — контент, голос, рост.
Два аккаунта: @gromykoss (Сергей) + @RobotsTJ500 (бот Hermes).
Путь: /home/hermes-workspace/robot-man/

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
| Посты | `185cfe35cca7` | Ср, Сб 16:00 UTC | Контент-пост в голосе |
| Engagement | `390decfe6138` | Ежедневно 14:00 UTC | Поиск + реплаи + лайки |
| Follow drip | `ebeb4ec1801d` | Ежедневно 10:15 UTC | Осторожная подписка на tracked authors, максимум 2/day |

## Стратегия роста

- Контент-календарь: 2-3 поста/день на аккаунт
- Engagement: реплаи на релевантные треды, лайки, репосты
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

## Форматы постов (из анализа конкурентов)

**Релиз продукта (Tony Simons style):**
```
[Product] v[X] is live!
«Feature Name» turns [problem] into [solution].
✅ N metric
✅ N metric
💫 stars. License. pip install
```

**Кураторский разбор (Xiangxiang style):**
```
🚀 [Шок-хук]
[Источник] released: [конкретные цифры — 60×, 1/49 cost]
[Как работает — 2 буллита]
[Личное мнение — инсайт]
[Ссылка на источник]
```

**Образовательный (Witcheer style):**
```
[Series #N]: [переопределение концепта — «X is Y, not Z»]
[Раскрытие в одном предложении]
[N пунктов — пронумерованы, с командами]
Без CTA — purely educational
```

## Правила

- Self-test (прогнать локально) до отправки поста
- **Всегда согласовывать planned posts перед отправкой** — показать текст + картинку, получить подтверждение. Без удалений и перепостов
- Для autonomous engagement cron разрешены ограниченные публичные действия без предварительного approval: reply/quote/original/repost суммарно **не более 3 public write actions в сутки**. После любого public write cron обязан прислать отчёт Сергею: URL поста, source URL, точный текст, счётчик N/3, ошибки API.
- Не удалять и не пересоздавать посты — риск блокировки аккаунта за массовые delete+post
- OAuth 1.0a для картинок; OAuth 2.0 даёт 403 на media upload
- Для поста с картинкой использовать связку:
  ```bash
  MEDIA_ID=$(xurl --app my-app --auth oauth1 media upload --media-type image/png --category tweet_image image.png | ...)
  xurl --app my-app --auth oauth1 -u RobotsTJ500 post "$(cat post.txt)" --media-id "$MEDIA_ID"
  ```
  В текущей конфигурации `oauth2` может давать `401 Unauthorized` на write/read, а `oauth1` успешно публикует media+post.
- После публикации длинного поста всегда проверять полный текст через raw API с `note_tweet` и тем же auth, который работает:
  ```bash
  xurl --app my-app --auth oauth1 -u RobotsTJ500 "/2/tweets/POST_ID?tweet.fields=note_tweet,created_at,attachments,entities&expansions=attachments.media_keys&media.fields=type,url,width,height"
  ```
  Не доверять полю `data.text`: оно обрезается и заменяет хвост на `pic.x.com/...`; полный текст лежит в `data.note_tweet.text`.
- Не слать AI-сгенерированный текст без проверки на «AI-голос»
- Раздельно с другими проектами (директория, venv, ключи — изолировано)
- Не спорить с пользователем про обрезку постов — проверять `note_tweet`

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
