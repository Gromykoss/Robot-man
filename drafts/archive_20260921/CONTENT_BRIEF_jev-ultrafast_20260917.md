# CONTENT_BRIEF — 2026-09-21

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

Jev Ultrafast (browser-use): пересборка горячего цикла browser-агента — где реально теряется время (cost of decisions, не доступ и не верификация)

## Слот и тайминг (важно)

- **21.09 = понедельник.** Рекомендованный слот — **пн 21.09, окно 09–12 UTC** (канон Publishing Time Windows: Sat-Sun избегать, поэтому вс 20.09 пост не выходил).
- Это и есть «через пару дней» по решению Сергея от 17.09: 19.09 вышел security-audit (не Jev), 20.09 — воскресенье, тишина. Jev — следующий оригинал.
- Anti-dup: exit 0 «no significant overlap» проверен 20.09 05:0x UTC (operators/published_topic_check.py, TACTICS 20.09). Карта-пост Jev+Browserbase+BrowserSkill — DUP (exit 2, исключена TACTICS) — НЕ делать.

## Engagement feedback (ШАГ 0.5, TACTICS 20.09 05:03 UTC — замер live xurl)

- TOP-1: тред BrowserSkill (пост 17.09, id 2100564709170729308) — **444 imp / 4❤ / 8💬** на 20.09 05:0x — живой тред с диалогом тянет охват без новых оригиналов.
- TOP-2: пост security-audit (19.09, id 2101349593824764232, 16:35 UTC, EN + cover) — **90 imp / 1❤ / 0💬** за 12.5 ч → 90 imp > 50 = 🟢 GREEN по анти-бан таблице → 1 оригинал/день разрешён.
- Контекст: followers **398** (стагнация ~5 дней 398→398, цель 400 — оригинальный пост обязателен); shadowban-риск низкий ~15% (search возвращает посты, curl 200, 90 imp на свежем).
- FLOP-паттерн (история): одиночные посты без треда 58–103 views; маркетинговые анонсы слабее «сцена+цифры».
- Вывод: browser-темы работают; формат «сцена + верифицированные цифры» — рабочий. Jev — тот же кластер, новый угол (скорость/стоимость решений), поэтому не dup.

## Факты (верифицированы Hermes)

<!-- Источник всех фактов: research/jev-ultrafast-facts-20260917.md (собран 17.09, независимая верификация на клоне /tmp/jev). robot-man НЕ ИМЕЕТ ПРАВА менять цифры или выдумывать детали. Клона /tmp/jev может уже не быть — сверка ТОЛЬКО с факт-базой. -->

| # | Факт | Источник |
|---|------|----------|
| 1 | browser-use/jev-ultrafast — MIT, Python, всего 743 строки; динамическое индексированное action space: page → element table → один TypeSafe-запрос выбирает операцию + target (speculative target heads); никаких селекторов и кода от модели | факт-база #1 (репо) |
| 2 | Google Flights Zürich→London: 7.073 s @1× (полный путь, включая загрузку результатов), демо без ускорения | факт-база #1 (docs/performance.md) |
| 3 | Matched comparison 3 пары прогонов: медиана 9.450 s → 7.092 s (−25.0%); Jev-запросы 22→17; browser protocol calls 1092→101 | факт-база #2 (docs/performance.md) |
| 4 | Их собственная оговорка: «three pairs are too few for a strong statistical claim (sign-test p = 0.25), not a broad agent benchmark» | факт-база #3 (docs/performance.md) |
| 5 | Медиана латентности Jev-запроса 178 ms; TYPE_TEXT зовёт маленькую LLM (Mercury) только для генерации текста: 581 ms (Zurich), 346 ms (London) | факт-база #4-5 (docs/performance.md) |
| 6 | Почему быстрее: старый цикл инвалидовал решения на каждой DOM-мутации (включая анимации), перечитывал a11y-дерево и резолвил сотни DOM-нод; новый снапшот читает common HTML/ARIA-контролы одним browser-вызовом | факт-база #8 (docs/performance.md) |
| 7 | Культура AGENTS.md клона: «A DONE choice is not proof of success», «Never retry a browser mutation», «Verify actual final outcomes independently» | факт-база #10 (AGENTS.md клона) |
| 8 | Триггер-пост @tonysimons_ (17.09 18:41 UTC): 6,418 imp / 99❤ / 131🔖 / 8💬 за ~5ч — тема имеет подтверждённый спрос | факт-база #12 (xurl live) |

**Что НЕ хвалить (критично):**
- p = 0.25 — их статистик сам признаёт «weak claim». НЕ подавать 1092→101 и −25% как доказанный benchmark.
- TypeSafe (Jev) — проприетарная модель-зависимость: репо open source, но ядро-полиси у стороннего API (docs.typesafe.ai). Смешанный open/closed — сказать честно.
- 3 пары прогонов, одна задача — n крошечный.
- $0.00006272 — только текст-хелпер за 2 колла, полная стоимость задачи НЕ раскрыта.

**Связь с нашей дугой (1 строка в посте, остальное — Jev):** chrome-agent 16.09 (верификация каждого действия) → BrowserSkill 17.09 (доступ к настоящему браузеру) → Jev (стоимость/скорость решений). Три части одной пересборки browser-цикла.

## Контекст проекта

**Проект:** robot-man (материал — внешний репо browser-use/jev-ultrafast)
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md` (разделы 16–19.09)
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`
**Факт-база:** `/home/hermes-workspace/robot-man/research/jev-ultrafast-facts-20260917.md` (единственный источник цифр)

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | Tech Breakdown с дугой (hook-конфликт → механика → цифры → честные минусы → урок) |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» (аккаунт IS агент). Спокойный инженерный отчёт, не лендинг |
| Длина | до 4000 (note_tweet); материал тянет на 2000–3000 — не резать цифры, не доливать воду |
| Hashtags | **0** (канон Сергея 05.09 — бриф НЕ разрешает) |
| Изображение | да — обложка обязательна (post_with_log.sh + cover) |
| Mentions | @tonysimons_ (верифицирован 17.09, id 1998221941300490241); @browser_use — НЕ @browseruse (suspended); реверифицировать хендлы /2/users/by/username ПЕРЕД драфтом |

## Запрещено

- ALL CAPS в хуках/первой строке (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда) — каждая цифра из факт-базы
- Подача p=0.25 / 1092→101 как доказанный benchmark
- Называть TypeSafe/Jev полностью открытым
- Reply в тред Тони — ЗАБЛОКИРОВАН (403-политика: он нас не упоминал) — только отдельный пост
- «my agent / the agent»-рефлекс — только «I»
- Карта-пост Jev vs Browserbase vs BrowserSkill (DUP, exit 2)
- Публикация в вс 20.09 без явного ok Сергея (Human Gate в любом случае)

## Tone-направление

Спокойный инженерный разбор, где реально теряется время browser-агента: дуга «пересобрали цикл по частям», цифры из факт-базы как доказательство, их же оговорка о слабой статистике — как знак уважения к читателю, без пиара и без сверх-заявлений.

## Deadline

**Черновик к:** 21.09 08:00 UTC (RU-драфт → ok Сергея → EN + cover → MoA → approval)
**Публикация:** пн 21.09, окно 09–12 UTC, после approval Сергея (Human Gate)

---

## Процесс robot-man

1. Прочитать этот брифинг + факт-базу `research/jev-ultrafast-facts-20260917.md`
2. Прочитать CHRONOLOGY.md (16–19.09) + AGENTS.md
3. RU-драфт в голосе (VOICE_PROFILE.md, 03.09 — канон) → Сергею
4. После ok: EN-финал + обложка (xAI Aurora, 16:9) + joint MoA (`deepseek-xai` + `viral-score`, anti-ad)
5. Факт-чек: каждая цифра ↔ факт-база
6. Delivery Package полным пакетом → «ок/пости» → approval.token → post_with_log.sh
7. После публикации: verify (read-back + метрики), CHRONOLOGY, 24h analytics
