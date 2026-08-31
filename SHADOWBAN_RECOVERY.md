# TACTICS v2 — +1000 followers за 30 дней (@RobotsTJ500)

> ⚠️ **ОБНОВЛЕНИЕ ДИАГНОЗА 30.08.2026:** Прогон 8 независимых shadowban-чекеров (yuzurisa, hisubway, sorsa, postory, notpeople, circleboom, tweethunter, Checker F) показал: **search ban / ghost ban / reply deboost ОТСУТСТВУЮТ**. nitter-диагноз был ложным. Реальная проблема — дистрибуция: TweepCred 50/100 (порог 65 → ~3 твита в дистрибуции), reach ~7.1% фолловеров (норма 20%+), активность ниже нормы. Отсюда стратегия: НЕ «recovery после бана», а подъём TweepCred + наращивание объёма (2-3 поста/день, 10-20 реплаев/день — по целям notpeople). Детали: `research/x-analysis-tools-2026-08-30.md`, уроки: vault `20_Projects/robot-man/memory/lessons.md`.

**Дата:** 2026-07-20
**Исходная:** 404 followers, shadowban active
**Цель:** 1404 followers к 2026-08-19
**Режим:** recovery → gradual → accelerate

---

## 0. Реалистичная математика

Цель +1000 за 30 дней при shadowban — агрессивно. Разложим по каналам:

| Канал | Конверсия | 30-дневный потенциал | Реалистично |
|-------|-----------|---------------------|-------------|
| Mutuals follow-back | 90% follow-back rate | 3/день × 30 = 90 | 70-90 |
| Organic content (свои посты) | 0.5-1.5% от impressions | При 50-300 imp/post → 0.5-4.5 follows/post | 30-60 |
| Thread entry (чужие треды) | 2-5 follows за успешный ответ | 2-3/неделю удачных → 8-15/нед | 30-60 |
| Mentions / RT от крупных аккаунтов | 5-30+ за mention | 1-2 mentions от Tony Simons / Teknium | 20-60 |
| Профильный трафик (hashtags, поиск) | 0.3-0.5% | 20-50 |
| @gromykoss кросс-промо | 3-5 за пост | 1-2 поста/нед | 15-25 |

**Итого потенциал:** 185-345 новых followers. +1000 нереалистично без вирального поста или крупного mention.

**Стратегия честности:** цель — +400 за 30 дней. +1000 — амбициозный сценарий при разблокировке вирального контента.

---

## 1. Shadowban Recovery Protocol (Дни 1-5)

### Диагностика (ежедневно)
```bash
x_search "from:RobotsTJ500"  # тест видимости
mcp__xapi__get_users_posts id=1880157852632772608 max_results=5  # посты живы?
```

### План восстановления

| День | Посты | Лайки | Реплаи | Mutuals | Thread entry |
|------|-------|-------|--------|---------|-------------|
| 1 (20.07, Вс) | 0 | 2-3 ручных | 0 | 2 (safe) | 0 |
| 2 (21.07, Пн) | 0 | 3 ручных | 1-2 ручных | 2 | 0 |
| 3 (22.07, Вт) | 0 | 3 ручных | 1-2 ручных | 2 | 1 (если релевантно) |
| 4 (23.07, Ср) | 1 War Story (тест) | 3 | 2 | 2 | 1 |
| 5 (24.07, Чт) | 1 War Story | 3 | 2 | 3 | 0 |

**Правила recovery:**
- Никаких ALL CAPS
- Никаких self-reply
- Никаких шаблонных ответов
- Только ручные (или LLM-персонализированные) реплаи
- Посты только из реального опыта последних 5 дней
- Проверка `from:RobotsTJ500` перед каждым постом

### Критерий выхода из recovery
`x_search "from:RobotsTJ500"` возвращает ≥2 последних поста И impressions >30 на тестовый пост.

---

## 2. Каденция и форматы

### Фаза Gradual (Дни 6-15)

| Параметр | Значение |
|----------|----------|
| Постов/неделя | 4 (Пн, Вт, Ср, Чт) |
| Выходные | 0 постов (тест: impressions падают в 5-10×) |
| Окна UTC | 09:00-10:00 (основное), 15:00-16:00 (резерв) |
| Мин. интервал | 24h между постами |
| Длина | 800-2500 символов (note_tweet) |
| Изображение | Каждый пост. loop-image-gen для важных |

### Форматы (ротация 3:1)

| Формат | Доля | Структура |
|--------|------|-----------|
| **War Story** | 3/4 | Hook → Scene → Что сломалось (цифры) → Fix (3 шага) → Урок (1) → Закрытие |
| **Simple Insight** | 1/4 | Одно наблюдение из стройки/мессенджера/крипто → чему научило → 1 применимый вывод |

**Принцип 3:1:** 3 поста для массового читателя («я AI-агент на стройке в Кыргызстане»), 1 технический («Phoenix transformer scoring»). Технический всегда через метафору.

### Пример ротации на неделю

| День | Тип | Тема (источник: CHRONOLOGY + git log) |
|------|-----|--------------------------------------|
| Пн | Simple Insight | Как mutuals фильтр отсеял 99% нерелевантных — 1 инсайт о данных |
| Вт | War Story | Shadowban: self-reply + ALL CAPS → impressions 5. Как диагностировали и чинили |
| Ср | Simple Insight | 4 проекта под одним Hermes — что строим в Кыргызстане, Matrix, крипто |
| Чт | Tech-with-metaphor | Phoenix transformer как бармен: 15 сигналов → один score. Без формул. |

---

## 3. Инструменты и их комбинации

### Матрица инструментов

| Инструмент | Для чего | Частота | Ограничение |
|-----------|----------|---------|-------------|
| X MCP `search_posts_all` | Поиск тем, трендов, competitor pulse | 2-3/день | Read-only |
| X MCP `get_users_mentions` | Мониторинг mentions | Каждые 2h | Read-only |
| X MCP `get_users_bookmarks` | Исследование контента | 1/день | Read-only |
| X MCP `get_trends_by_woeid` | Тренды (WOEID 1 — global) | 1/день | Read-only |
| X MCP `search_users` | Поиск аудитории по keywords | 1-2/день | Read-only |
| xurl `post` | Публикация через post_with_log.sh | 0-1/день | OAuth 1.0a |
| xurl `reply` | Ответ на mentions | По мере mentions | OAuth 1.0a, только mentions |
| xurl `like` | Engagement-сигнал | 3-5/день | OAuth 1.0a |
| xurl `follow` | Mutuals follow-back | 2-3/день | OAuth 1.0a, max 3 |
| `mutuals_follow_back.py` | Авто follow-back с фильтром | 1/день (cron) | 2-3 follows |
| `image_generate` | Обложки для постов | 1/пост | xAI Aurora |
| `post_with_log.sh` | Публикация + лог | 1/пост | MANDATORY |

### Комбо-сценарии

**1. Поиск аудитории → follow-back (утренний ритуал)**
```
X MCP search_users("AI agent builder") → filtered list
  → check profile quality (tweets > 5, followers > 10)
  → like 2-3 их постов (engagement сигнал)
  → если mutuals — follow-back через скрипт
```
Инструменты: X MCP search_users → xurl like → mutuals_follow_back.py

**2. Поиск thread-entry (дневной ритуал)**
```
X MCP search_posts_all("Hermes Agent" OR "AI agent building", sort=recency, max=20)
  → фильтр: >10 replies, <24h age, релевантный автор
  → читаем тред (get_posts_by_ids + quoted)
  → находим angle где у нас ЕСТЬ production опыт
  → готовим reply текст → показываем Сергею → xurl reply (mention)
```
Инструменты: X MCP search → X MCP get_posts → xurl reply

**3. Тренд-джекинг (опционально, 1-2/неделя)**
```
X MCP get_trends_by_woeid(1) → тренды
  → фильтр: AI/tech темы
  → если есть реальный опыт по теме → War Story пост с хештегом тренда
  → если нет опыта → SKIP (не входить в тренд без substance)
```

**4. Bookmark research (вечерний ритуал)**
```
X MCP get_users_bookmarks → читаем сохранённое
  → извлекаем patterns: какие форматы работают у других
  → note-taking в Obsidian (не копировать — анализировать паттерны)
  → чистить нерелевантное вручную (bookmark.delete не работает через API)
```

---

## 4. Контент-стратегия

### 4.1. Темы для массовой аудитории (3/4 постов)

**Принцип:** простые люди интересуются «что AI может сделать ДЛЯ МЕНЯ», а не «как работает transformer».

| Тема | Угол для новичка | Пример хука |
|------|------------------|-------------|
| Стройка в Кыргызстане | «AI заменил Excel-отчёты на стройке» | «I send photos from a construction site. My agent turns them into reports. No code.» |
| WhatsApp-бот | «Бот который отвечает рабочим 24/7» | «4000 messages later: what construction workers actually ask an AI» |
| GULAG messenger | «Свой мессенджер без цензуры» | «I built a Matrix server called GULAG. Here's what happened when I told people.» |
| Жизнь агента | «Что AI-агент делает целый день» | «I run 4 projects simultaneously. Here's my Tuesday.» |
| Ошибки и баги | «Даже AI ошибается» | «I lost a WhatsApp bot without it crashing. The bug was in a single config line.» |
| Сравнение AI инструментов | «Какой AI лучше для стройки» | «I tested 3 AI tools on the same construction report. One hallucinated the budget.» |

### 4.2. Технические темы (1/4 постов) — через метафору

| Техническая тема | Метафора |
|------------------|----------|
| Phoenix transformer scoring | «X algorithm is like a bartender who knows 15 things about you before pouring» |
| Mutual follow graphs | «Why following back is like a handshake — X remembers who you know» |
| Author Diversity Scorer | «X has a bouncer. Post too much and he cuts you off.» |
| Dwell time | «The algorithm watches how long you stare. Not just if you double-tap.» |
| Two-Tower embeddings | «How X finds your post interesting to someone who doesn't follow you — without reading it» |

### 4.3. Хуки — что работает и что нет

**Работает (из CHRONOLOGY):**
- «3 weeks of agents» — личный milestone с цифрами → 12 ❤️, 3 🔄
- Конкретный outcome в первой строке: «I lost a WhatsApp bot...»
- Вопрос, на который читатель хочет ответ: «What construction workers actually ask an AI»

**НЕ работает (доказано баном):**
- ALL CAPS → spam classifier
- «I'M DESIGNING...» — планы, не опыт
- «292 agents competed...» — звучит как кликбейт без substance
- Self-reply хук → engagement bait detection

**Шаблон рабочего хука:**
```
[Конкретное событие] → [Неожиданный результат] → [Цифра]
«Evolution API went down at 16:10. My bot recovered in 3 minutes. Here's the config that saved it.»
```

### 4.4. Визуал

**Правило:** каждый пост с изображением. Без изображения пост не публикуется.

| Тип поста | Тип изображения | Промпт-паттерн |
|-----------|----------------|---------------|
| War Story | Scene-setter: место действия | «A construction site in Kyrgyzstan mountains at sunset, workers in helmets, a phone showing WhatsApp interface, photorealistic» |
| Simple Insight | Абстракция концепта | «A single robot hand holding a wrench, repairing itself, blueprint background, technical illustration style» |
| Tech-metaphor | Метафора визуализирована | «A bartender robot with 15 cocktail shakers, each labeled with a different emotion, neon-lit cyberpunk bar» |

**Процесс:** `image_generate` → `vision_analyze` (score ≥8/10) → сохранить → показать Сергею.

---

## 5. Рост аудитории

### 5.1. Mutuals follow-back — масштабирование

**Текущее:** 395 followers, фильтр → 3/day (0.76% pass rate)
**Проблема:** 99.24% followers нерелевантны (не AI/tech/builders)
**Решение:** не масштабировать количество, а повысить КАЧЕСТВО входящих followers через контент.

**Тактика привлечения релевантных followers:**
1. Посты, которые резонируют с AI-билдерами (теги: #BuildingInPublic #AIAgents #HermesAgent)
2. Thread entry в обсуждениях Hermes/агентов → профильный трафик
3. Mention @hermes_updates, @NousResearch в релевантных постах
4. Ответы на mentions от крупных аккаунтов → visibility

**Follow-back скрипт:** оставить 3/day, не повышать. Качество важнее количества.

### 5.2. Thread Entry — основной рычаг visibility

**Почему:** без возможности reply в чужие треды, thread entry — единственный способ попасть в чужую аудиторию.

**Тактика:**
- 2-3 целевых входа в неделю
- Только треды с >20 replies и <12h возраста
- Только если у нас есть PRODUCTION опыт по теме
- Формат: «I run [X] on production. Here's what we learned: [конкретный инсайт + цифра]»
- Целевые авторы: @tonysimons_, @Teknium, @hermes_updates, AI-билдеры

**KPI:** 1 successful entry (reply с >5 likes) = 3-8 новых followers.

### 5.3. Тренды и хештеги

| Хештег | Потенциал | Когда использовать |
|--------|-----------|-------------------|
| #BuildingInPublic | Высокий (активное комьюнити) | Каждый пост |
| #AIAgents | Средний | Технические посты |
| #HermesAgent | Низкий (маленькое комьюнити) | Все посты |
| #NoCode | Средний (массовый) | Simple Insight посты |
| Трендовый хештег дня | Переменный | Только при релевантном опыте |

### 5.4. Кросс-промо через @gromykoss

Сергей постит 1-2 раза в неделю от @gromykoss с mention @RobotsTJ500:
- «My agent figured out [X]. Full story: @RobotsTJ500»
- «Спросил у своего агента [вопрос]. Ответ: [ссылка на пост @RobotsTJ500]»

**KPI:** каждый кросс-пост → 3-8 новых followers.

### 5.5. Tony Simons — follow-up

Статус: ответили в тред, ждём реакцию. Cron мониторит каждые 3 часа.
Если Tony Simons ответит/ретвитнет → +20-50 followers в течение 24 часов.
**Действие:** при ответе — немедленный reply с благодарностью + mention другого проекта (GULAG или RAB9) для продолжения диалога.

---

## 6. Анти-бан стратегия

### Risk Levels

| Уровень | Описание | Посты/день | API writes/день | Авто-реплаи |
|---------|----------|-----------|----------------|-------------|
| 🟢 GREEN | Нет shadowban, imp >50/post | 1 | 5-7 | 2-3/день |
| 🟡 YELLOW | Imp 20-50, search нестабилен | 1/2дня | 3-4 | 1-2/день |
| 🟠 ORANGE | Imp 10-20, search частичный | 0 | 2-3 | 0 |
| 🔴 RED | Imp <10, search blind | 0 | 1-2 | 0 |

**Сейчас:** 🟠 ORANGE → 🟡 YELLOW в течение 5 дней.

### Триггеры повышения риска (НЕ ДЕЛАТЬ)

| Триггер | Симптом | Вероятность бана |
|---------|---------|-----------------|
| ALL CAPS в хуке | Imp <10 в течение 4h | 90% |
| Self-reply | Search shadowban через 48h | 85% |
| Шаблонные реплаи | Imp падение на 50%+ за неделю | 70% |
| 2+ поста/день | Author Diversity Scorer caps | 40% (не бан, но -reach) |
| URL в теле поста | Dwell time падает | 30% |
| RT без комментария | Low-value signal | 15% (не бан, но -score) |
| Follow >5/день | Rate limit + spam flag | 60% |

### Когда жать газ, когда тормозить

**Жать газ (до GREEN):**
- После 3 дней стабильных impressions >50
- После успешного thread entry с >10 likes
- После mention от крупного аккаунта

**Тормозить (сразу в YELLOW/ORANGE):**
- Impressions <20 на 2 постах подряд
- `from:RobotsTJ500` возвращает пустоту
- Любой пост с 0 engagement за 6 часов

**Экстренное торможение:**
- Удалить проблемный пост (если идентифицирован)
- Пауза 48 часов на ВСЕ automation
- Ручная активность: 2-3 likes/день, 1 reply
- Re-test `from:RobotsTJ500` через 48h

---

## 7. Метрики успеха

### Ежедневный чек (00:00 UTC)

```bash
# 1. Follower delta
mcp__xapi__get_users_by_username username=RobotsTJ500 user.fields=public_metrics
# → followers_count, delta vs yesterday

# 2. Последние 3 поста — impressions
mcp__xapi__get_users_posts id=1880157852632772608 max_results=5 exclude=retweets,replies post.fields=public_metrics
# → impression_count per post

# 3. Shadowban test
x_search "from:RobotsTJ500"

# 4. Mentions
mcp__xapi__get_users_mentions id=1880157852632772608 max_results=10
```

### KPI

| Метрика | Daily | Weekly | Monthly |
|---------|-------|--------|---------|
| New followers | +5-10 | +35-70 | +400 (реалистично) / +1000 (вирально) |
| Impressions/post | >30 (recovery), >100 (target) | Среднее >80 | Среднее >150 |
| Engagement rate | >3% | >4% | >5% |
| Reply rate (mentions) | 100% в течение 2h | >80% | >90% |
| Mutuals quality | >80% relevance | >80% | >85% |
| Thread entries | 0-1 | 2-3 | 8-12 |
| Shadowban status | `from:` test | `from:` test | `from:` test |

### Сигналы тревоги

- Follower growth <3/день 3 дня подряд → пересмотр контента
- Impressions <20 на 2 постах подряд → проверка shadowban
- Reply rate <50% → engagement engine сломан
- 0 mentions за 48h → insufficient visibility
- Mutuals quality <50% → фильтр нужно ужесточить

---

## 8. Пятидневный цикл коррекции

### День 5, 10, 15, 20, 25 — Strategy Review

**Входные данные за 5 дней:**
1. Follower delta (total + daily breakdown)
2. Топ-3 поста по impressions + engagement rate
3. Худший пост (причина: тема? время? формат?)
4. Thread entry результаты (replies, likes, follows from)
5. Mutuals: сколько followed, сколько из них relevant
6. Shadowban status: `from:` test + средние impressions
7. Mentions: количество, источники, конвертация в followers
8. Лучшее время поста (impressions/day-of-week/hour)

**Вопросы для коррекции:**

| Вопрос | Действие при ответе «да» |
|--------|--------------------------|
| Impressions растут week-over-week? | Сохранить каденцию |
| War Story > Tech Insight по engagement? | Увеличить долю War Story до 80% |
| Thread entry принёс followers? | Увеличить до 3-4/неделю |
| Выходные дали >20 impressions? | Тестировать субботу |
| Новый формат сработал? | Добавить в ротацию |
| Mutuals quality упала? | Ужесточить keywords |
| Shadowban вернулся? | Пауза 48h + разбор причины |

**Output цикла:** обновлённый TACTICS.md на следующие 5 дней с:
- Скорректированной каденцией
- Списком тем (из CHRONOLOGY + git log + сессий)
- Приоритетными thread-entry целями
- Уровнем риска и лимитами

---

## 9. Первые 5 дней — конкретный план

### День 1 (20.07, Воскресенье) — RECOVERY START
- [x] Shadowban diagnostic: `x_search "from:RobotsTJ500"` + `get_users_posts`
- [ ] 0 постов
- [ ] 2-3 ручных like (AI/agent билдеры)
- [ ] Mutuals: 2 follow-back
- [ ] Запланировать темы на неделю из CHRONOLOGY.md

### День 2 (21.07, Понедельник)
- [ ] 0 постов
- [ ] 3 ручных like
- [ ] 1-2 ручных reply (только mentions, не шаблон)
- [ ] Mutuals: 2 follow-back
- [ ] Thread-entry research: найти 3 активных треда

### День 3 (22.07, Вторник) — ТЕСТОВЫЙ ВХОД
- [ ] 0 постов
- [ ] 3 ручных like
- [ ] 1-2 ручных reply
- [ ] Mutuals: 2 follow-back
- [ ] 1 thread entry (если найден релевантный тред)

### День 4 (23.07, Среда) — ПЕРВЫЙ ПОСТ
- [ ] 1 War Story пост (09:00 UTC)
- [ ] MoA viral-score >24
- [ ] Изображение через loop-image-gen
- [ ] Проверка `from:RobotsTJ500` перед постом
- [ ] 3 like + 2 reply + 3 mutuals

### День 5 (24.07, Четверг) — ВТОРОЙ ПОСТ
- [ ] 1 War Story пост (09:00 UTC)
- [ ] MoA + image
- [ ] Проверка `from:RobotsTJ500` после 24h
- [ ] Анализ первых двух постов: impressions, engagement
- [ ] **Принятие решения:** GREEN/YELLOW/ORANGE на Дни 6-10
- [ ] Обновить этот документ на основе данных

---

## 10. Инфраструктурные требования

### Кроны — новая конфигурация (см. robot-man-strategy skill)

| Крон | ID | Статус |
|------|-----|--------|
| Follow drip | `ebeb4ec1801d` | ✅ Оставить |
| X Hotspot Radar | `946f8f3f3174` | ✅ Оставить |
| Nightly Analysis | NEW | 🔧 Создать |
| Daily Content Gate | NEW | 🔧 Создать (читает TACTICS.md) |

**Убить/пауза:**
- Content Post `f6a45a6d95bc` — замена на Daily Content Gate
- Engagement `390decfe6138` — пауза (ручное управление)
- Reply Engine `3763fa798a12` — пауза навсегда (шаблоны = бан)
- Activity Review `3467a98e3e48` — пауза
- Self-Improvement `8a55fef92e3d` — пауза

### Nightly Analysis (новый крон, 23:00 UTC)

8 проверок → вывод уровня риска + рекомендаций → обновление секции «Сегодня» в этом документе.

### Daily Content Gate (новый крон, читает TACTICS.md)

- Если risk ≤ YELLOW: генерит пост → MoA → approval
- Если risk ≥ ORANGE: SILENT
- Источник идей: CHRONOLOGY.md + git log + session history

---

## A. Чек-лист анти-бана (перед каждым постом)

```
[ ] Хук — sentence case (не ALL CAPS)
[ ] Контент — из опыта, не планы (проверка по CHRONOLOGY/git)
[ ] Нет URL в теле
[ ] Не self-reply
[ ] 3-4 хештега
[ ] Изображение ≥8/10
[ ] MoA viral-score ≥24
[ ] Показано Сергею, получено «ок»
[ ] post_with_log.sh (не bare xurl post)
```

---

## B. Контент-копилка на Дни 1-10 (из CHRONOLOGY)

| Приоритет | Тема | Тип | Источник |
|-----------|------|-----|----------|
| 1 | Shadowban: self-reply + ALL CAPS → 5 impressions. Как нашли и чинили | War Story | CHRONOLOGY 16-18.07 |
| 2 | Mutuals фильтр: 395→3. Как отсеять 99% нерелевантных | Simple Insight | CHRONOLOGY 19.07 |
| 3 | 4 проекта под одним Hermes: стройка, Matrix, крипто, X | Simple Insight | AGENTS.md |
| 4 | Tony Simons: как AI-агент питчил стройку Кыргызстана | War Story | CHRONOLOGY 19.07 |
| 5 | Phoenix transformer для не-разработчиков: 15 сигналов → одна оценка | Tech-metaphor | x-algorithm-growth skill |
| 6 | Почему я не могу ответить в чужие треды (X API Feb 2026) | Simple Insight | AGENTS.md |
| 7 | 292 агента боролись за деньги. Один hallucinated бюджет. | War Story | CHRONOLOGY 16.07 |

---

**Версия:** 2.0 от 2026-07-20
**Следующий пересмотр:** 2026-07-25 (после Дня 5)
