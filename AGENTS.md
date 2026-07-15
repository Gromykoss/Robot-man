# Robot-man — X/Twitter AI-аккаунты и раскрутка

Проект: AI-управление X-аккаунтами — контент, голос, рост.
Два аккаунта: @gromykoss (Сергей) + @RobotsTJ500 (бот Hermes).
Путь: /home/hermes-workspace/robot-man/

## Старт сессии

1. `skill_view("hermes-self-knowledge")` — 14 паттернов харнеса
2. `skill_view("build")` — общие правила строительства
3. Прочитай `~/hermes-vault/30_Logs/Арсенал Hermes.md`
4. Затем этот файл

## Архитектура

Voice Data (реплаи) → Voice Profile → Content Pipeline → xurl → X
                                     ↑
                              Strategy Engine (темы, каденция, рост)
                                     ↑
                              Analytics (engagement, follower delta)

## Инструментарий

- **xurl** — официальный CLI X API: пост, реплай, квот, DM, медиа, поиск
- **voice-match skill** — голосовые профили
- **Метод Мэтта (Train Voice):** реплаи > посты

## Аккаунты

| Аккаунт | Для чего | Тип контента |
|---------|----------|-------------|
| @gromykoss | Личный бренд, AI/билдинг | Мысли, наблюдения, ирония |
| @RobotsTJ500 | AI-агентность, техника | Технические инсайты, кейсы |

## Быстрые команды

```bash
xurl auth status
xurl whoami
xurl post "текст"
xurl search "query" -n 10
xurl search "from:USERNAME" -n 20
```

## Голосовые профили

- **@gromykoss:** тёплый, ироничный, сторителлинг. Полный профиль: `VOICE_PROFILE_GROMYKOSS.md`
- **@RobotsTJ500:** технический, прямой, без эмодзи. Полный профиль: `VOICE_PROFILE.md`

## Файлы проекта

| Файл | Для чего |
|------|----------|
| `AGENTS.md` | Контекст для Hermes |
| `CONTENT_STRATEGY.md` | Темы, каденция, тактика роста |
| `VOICE_PROFILE.md` | Голос @RobotsTJ500 |
| `VOICE_PROFILE_GROMYKOSS.md` | Голос @gromykoss |
| `analytics.py` | Еженедельная аналитика |
| `engage.py` | Engagement engine |
| `scripts/analytics_loop.py` | Self-improvement loop |
| `skills/*/SKILL.md` | Specialist skills (x-researcher, content-writer и др.) |

## Cron-джобы (ID сохранять)

| Джоб | ID | Расписание | Что делает |
|------|-----|-----------|------------|
| Аналитика | `87832edf5bc3` | Пн 10:00 UTC | Еженедельный отчёт |
| Посты | `185cfe35cca7` | Ср, Сб 16:00 UTC | Контент-пост (post_with_log.sh) |
| Engagement | `390decfe6138` | Ежедневно 14:00 UTC | Поиск + реплаи + лайки |
| Follow drip | `ebeb4ec1801d` | Ежедневно 10:15 UTC | Осторожная подписка (max 2/day) |
| Reply Engine | `3763fa798a12` | Каждые 30 мин | Ответы на комментарии |
| Self-Improvement | `8a55fef92e3d` | Ежедн 15:00 UTC | analytics_loop + voice update |

## X API: ограничения reply (июль 2026)

**Вердикт:** Ответы в чужие треды через API НЕВОЗМОЖНЫ (X заблокировал Feb 2026). Работает только mentions.

**Стратегия (4 пути):** 1. Mentions (`xurl mentions`), 2. Пост с URL, 3. Рост упоминаний, 4. Подготовка текста → Сергей постит вручную.

## X API: длинные посты (Premium)

Premium (4000 символов) — полный текст в `note_tweet.text`. Всегда запрашивать `tweet.fields=note_tweet`.

```bash
xurl --app my-app --auth oauth2 -u '@user' "/2/tweets/ID?tweet.fields=note_tweet"
xurl post --app my-app --auth oauth2 -u '@user' "полный текст до 4000 символов"
```

## MoA проверка постов (v3)

| Пресет | Reference | Aggregator | Когда |
|--------|-----------|------------|-------|
| `deepseek-xai` | grok-4-latest | deepseek-v4-pro | Hook + voice |
| `viral-score` | grok-4-latest | deepseek-v4-pro | Hook(1-10) + engagement(1-10) + virality(1-10) |

Оба agree → пост. Иначе — переписать.

## Голос и стиль @RobotsTJ500

- First-person «I», English only
- Practical guide > report
- «Building in public. 🤖» — завершение
- #hashtags обязательны, нет URL в теле
- Одна верификация на сессию

## Изображения

- Провайдер: xAI Aurora (landscape 16:9)
- **Loop (skill `loop-image-gen`):** Maker (`image_generate`) → Checker (`vision_analyze`) → PASS
- Для важных — loop, для простых — 1 промпт. Цель 8-10/10

## Стратегия контента (v2)

**Каденция:** 2 поста/день (утро 10-12 UTC, вечер 16-18 UTC). Каждый с изображением. Мин 4 часа между. Подтверждение Сергею перед постом.

**Форматы приоритета:**
1. **War Story** (~70%): Проблема → что сломалось (цифры) → как чинил (3-5 пунктов) → урок → Building in public. 🤖 + 3-4 hashtags
2. **Технический разбор** (~20%): Релиз/фича → как применить (без маркетинга, без URL в теле)
3. **Квот-твит** (~10%, max 1/нед): + свой инсайт

**Антипаттерны:** Хук без раскрытия, квот без мнения, URL в теле, 3+ постов/день, чисто образовательный без опыта.

**Engagement:** Отвечать на КАЖДЫЙ комментарий в течение 2 часов. Цель reply rate >50%.

## Архитектура (v3)

### Полный поток

Идея → RESEARCH (x-researcher) → WRITE (content-writer) → EDIT (content-editor + MoA) → VIRALITY (/moa viral-score) → IMAGE (loop-image-gen) → APPROVAL (Сергей) → PUBLISH (post_with_log.sh) → Reply Engine → ANALYTICS (24h) → VOICE UPDATE

### Компоненты

| Компонент | Файл | Назначение |
|-----------|------|-----------|
| **xurl CLI** | системный | X API |
| **post_with_log.sh** | `post_with_log.sh` | Публикация + лог |
| **analytics.py** / `analytics_loop.py` | scripts/ | Метрики + self-improvement |
| **engage.py** / `reply_to_comments.py` | . | Engagement |
| **follow_tracked_authors.py** | . | Cautious follow (dry-run default, max 2/day) |

### Specialist Pipeline

```bash
skill_view("x-researcher")
skill_view("content-writer")
/moa viral-score
/moa deepseek-xai
loop-image-gen → show Sergey → post_with_log.sh
```

Все skills в `robot-man/skills/<name>/SKILL.md`.

### Self-Improvement Loop

[24h after publish] → analytics_loop.py (метрики, классификация, паттерны) → voice-updater (suggestions в VOICE_PROFILE.md) → human review.

### X API доступный функционал (@RobotsTJ500)

| Операция | Статус | Аутентификация |
|----------|--------|---------------|
| Читать посты, search, mentions | ✅ | OAuth 1.0a/2.0 |
| Постить текст/медиа | ✅ | OAuth 1.0a |
| Reply (свои + mentions) | ✅ | OAuth 1.0a |
| Like / Repost / Follow | ✅ | OAuth 1.0a |
| DM / Удалить свои | ✅ | OAuth 1.0a |
| Reply чужим / Quote | ❌ | X блок Feb 2026 |

## Правила строительства

### ⛔ PRE-PATCH GATE (MANDATORY — все проекты)

Перед любым изменением кода:
1. `grep -rn "имя" .` — все места использования функции/переменной
2. Показать grep в ответе пользователю
3. Проследить логику в КАЖДОМ найденном месте
4. Только потом патч

Если grep не показан — патч не принят. Откат.

## Agent-Driven Development Rules (Codex CLI / Grok Build)

**Загрузить перед делегированием:** `skill_view('codex-grok-delegation')`

При делегировании задач в Codex CLI или Grok Build:

1. **Read docs first** — прочитать этот AGENTS.md + `CHRONOLOGY.md` перед любым изменением
2. **Use build plan** — для задач >20 строк: Шаблон 1 из `codex-grok-delegation` (Goal Mode). Для постов — pre-post чеклист (пункт 4)
3. **Preserve security** — НЕ обходить OAuth, не постить без MoA-проверки, не превышать лимиты (max 3 writes/сутки)
4. **Verification ladder** — `xurl auth status` → MoA → vision_analyze → `cronjob list` → Сергей → post_with_log.sh → CHRONOLOGY.md
5. **Reproducible setup** — использовать `post_with_log.sh` для публикаций, не изобретать параллельные пути
6. **No production without approval** — посты только после явного «ок» Сергея. Follow: dry-run default
7. **Never expose credentials** — OAuth токены, xurl конфиг — не коммитить, не логировать
8. **Preserve user changes** — `git status` перед работой, не перезаписывать чужие правки

### 0. Авто-ведение документации — MANDATORY
AGENTS.md и CHRONOLOGY.md обновляются автоматически.

### 1. Контент — качество > количество
- MoA проверка обязательна (`/moa deepseek-xai`)
- Каждый пост с изображением (8-10/10)
- 2 поста/день max, мин 4 часа
- Форматы: War Story (70%) > Tech (20%) > Quote (10%)

### 2. Подтверждение перед отправкой — MANDATORY
Показать Сергею текст + картинку → явное «ок» → `post_with_log.sh`

### 3. Инфраструктуру верифицировать при старте
- `xurl auth status`
- `cronjob list` (фильтр robot-man)
- `cat published_posts.jsonl | tail -3`
- API лимиты в ответе

### 4. Pre-post чеклист (v3)
1. RESEARCH: x-researcher
2. WRITE: content-writer (VOICE_PROFILE.md)
3. EDIT: content-editor + MoA
4. VIRALITY: /moa viral-score
5. Изображение (loop если важно)
6. vision_analyze 8-10/10
7. Показать Сергею
8. `post_with_log.sh` → ID в published_posts.jsonl
9. 24h: analytics_loop → voice update

### 5. API-лимиты и безопасность
- OAuth 1.0a для write
- Max 3 public writes/сутки (autonomous)
- После write → отчёт Сергею
- Cautious follow: max 2/day (hard 3)
- 429 → STOP

### 6. Правило отката
```bash
xurl --app my-app --auth oauth1 -u RobotsTJ500 tweet delete POST_ID
```
Не злоупотреблять.

### 7. Баги → документ
BUGS.md (ID, симптом, причина, fix, статус)

### 8. Self-test перед отправкой
RESEARCH / WRITE / EDIT / VIRALITY / Изображение / Формат / note_tweet / 24h analytics

## Cautious Follow Workflow
Tracked-author follows: gradual, auditable. Default cap 2/day, hard 3/day only with explicit instruction. Use `follow_tracked_authors.py` (dry-run default, `--execute` for side effects). Stop on 429/403. Never mass follow or churn.