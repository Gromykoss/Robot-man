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
