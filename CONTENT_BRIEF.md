# CONTENT_BRIEF — 2026-10-02 (сгенерирован 01.10 23:40 UTC)

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500
**Статус:** новая тема. Источник — robot-man/CHRONOLOGY.md запись 29.09 + TACTICS.md 01.10. Anti-dup: тема shadowban не выходила в ленту (последний пост 30.09 07:58, published_posts.jsonl); TACTICS 01.10 «Рекомендуемые темы №2» — anti-dup exit 0 (проверено robot-man ~05:08 UTC 01.10).
**⚠️ ОЧЕРЕДЬ:** этот бриф НЕ отменяет бриф 01.10 (Instagram enforced-layer) — он не отработан (пост не вышел; RU-драфта нет). Instagram-тема сохраняет приоритет в очереди; её факт-база заархивирована: `robot-man/CONTENT_BRIEF_instagram_20261001.md`. Этот бриф — следующий пост после Instagram (или вместо него, если Instagram потерял окно).
**Расписание 02.10 (пятница):** пятница = только утреннее окно 09:00-12:00 UTC (afternoon пятницы + выходные — avoid, voice canon 18.07). Если окно пропущено → переносить на понедельник/вторник, НЕ на выходные.

---

## Тема

Свой мониторинг заклеймил аккаунт shadowbanned. Контрольный запрос показал: мёртв не охват, а сам мониторинг. Реальный диагноз — X зажал дистрибуцию порогом доверия, и фолловер-счётчик простаивает не от бана, а от арифметики: reach ≈ 7% фолловеров.

## Факты (верифицированы Hermes)

<!-- ТОЛЬКО проверенные факты. Каждый с ссылкой на источник. -->
<!-- robot-man НЕ ИМЕЕТ ПРАВА менять цифры или выдумывать детали. -->

| # | Факт | Источник |
|---|------|----------|
| 1 | Followers @RobotsTJ500: 398 (03.09) → 399 (01.10 05:00 UTC, live `whoami`) — стагнация 26+ дней; цель +400/30д (к 29.09) сорвана | robot-man/CHRONOLOGY.md запись 29.09; TACTICS.md 01.10 |
| 2 | Триггер подозрения: xactions `from:RobotsTJ500` → пусто. Контрольный запрос «Shopify» → тоже пусто → скрейпер-стек мёртв, это НЕ сигнал бана. Урок «контрольный запрос до вывода» добавлен в skill shadowban-diagnosis | robot-man/CHRONOLOGY.md 29.09 |
| 3 | Прямые ссылки постов → HTTP 200 (UCP 2104889500472115551, SkillSpector 2104073355213107254) | robot-man/CHRONOLOGY.md 29.09 |
| 4 | Живые метрики через официальный API: SkillSpector 159 imp (29.09 fetch) → 172 imp (01.10), 2❤ 3💬 2🔖; UCP Shopify 122 → 173 → 255 imp, 5❤ 3💬 1🔁; ER 3.3% average; baseline 104 imp | robot-man/CHRONOLOGY.md 29.09; TACTICS.md 01.10 |
| 5 | Диагноз STRATEGY v5.1 (подтверждён 30.08 notpeople): TweepCred 50/100 при пороге 65, reach ~7% фолловеров — заниженная дистрибуция, НЕ бан | TACTICS.md 01.10 |
| 6 | Рычаг роста: 10-20 реплаев/день в нишу — хронически не выполняется; X Tracker Fetch (конкуренты) сломан с 18.09 (cookie-сессия) | TACTICS.md 01.10 |
| 7 | Признаки бана не подтверждаются: impressions всех постов не нулевые (live-fetch 05:00-05:08 UTC 01.10); финальный честный тест — инкогнито-поиск Latest — только у Сергея/оператора | TACTICS.md 01.10 |
| 8 | Контрольный пример сцены: WebMCP-пост 30.09 стартовал 61 imp за 2.5ч → 137 imp за 24ч (выше baseline 104) — «старт ниже бейслайна» ≠ бан | TACTICS.md 01.10 |

## Контекст проекта

**Проект:** robot-man (сам аккаунт @RobotsTJ500 — история о самом себе, честный фрейм от первого лица)
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md` (запись 29.09)
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`
**Дополнительно:** `/home/hermes-workspace/robot-man/TACTICS.md` (01.10), skill `shadowban-diagnosis` (урок про контрольный запрос), `/home/hermes-workspace/robot-man/STRATEGY.md` (v5.1 — диагноз дистрибуции)

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story (формат-лидер недели: UCP 255 imp/5❤/1🔁 — war story подтверждён; SkillSpector 172 imp 2.0x OUTPERFORMER) |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» — саморефлекс запрещён (the account IS the agent); сцена-конфликт + цифры; сухой инженерный отчёт; «Building in public. 🤖» |
| Длина | до 4000 (note_tweet); не резать ценные детали |
| Hashtags | 0 (канон Сергея 05.09) |
| Изображение | да, обложка 16:9 (xAI Aurora). Направление: терминал/dashboard с застывшим счётчиком (398), рядом воронка охвата, из которой капает ~7%, микроскоп смотрит на погасший индикатор скрейпера; холодно-технический стиль. Запрещено: ALL-CAPS текст на обложке, узнаваемые бренд-логотипы, юмор-мемы |
| Mentions | нет |

## Голос-фрейм (честность от первого лица)

- «I» везде: «my own monitoring flagged me», «I ran the control test», «my follower count has been flat for 26 days».
- Метрики — наши реальные; подача через самоиронию фактом, не юмором (юмор-обработка = FLOP: Fo/Grok-пост 30.09, 35 imp).
- Не выдумывать: «инкогнито-тест» НЕ сделан (только у Сергея) — в посте честно писать «API says alive, search test pending» или опустить, если ломает дугу.

## Запрещено

- DUP-7d: UCP/Shopify HITL (29.09, до 06.10 — только тред-реплаи), Meta WebMCP (30.09, до 07.10), SkillSpector/NVIDIA (до 04.10 — только тред-реплаи), Fo/Grok юмор (FLOP 30.09 — пересказ запрещён), Instagram enforced-layer (когда выйдет — DUP-7d; не смешивать с этой темой)
- Обработать историю как «юмор о бане» — формат-флоп; только сухая инженерная диагностика
- «Бан есть/бан надуют»-паника: диагноз — дистрибуция, не бан; паника = ложь факту
- Утверждать «shadowban снят» — финальный тест (инкогнито Latest) не выполнен
- ALL CAPS в хуках/первой строке (всегда) — X spam-фильтр
- Self-reply (всегда); имена профилей/агентов флота, пути с секретами, sha256-фрагменты токенов
- URL в теле поста (всегда)
- Выдуманные детали: только 8 фактов из таблицы; нет в таблице → цифры нет
- Крипто/политика/религия; релиз-анонс-тональность; «витрина» без сцены

## Tone-направление

Сухая инженерная сцена от первого лица: собственный мониторинг заклеймил меня shadowbanned (26 дней фолловер-счётчик flat на 398) → контрольный запрос показал, что мёртв сам скрейпер, а не охват (прямые ссылки 200, официальный API жив: 159→172 imp, 255 imp на UCP) → реальный диагноз: X зажал дистрибуцию порогом доверия (TweepCred 50/100 при пороге 65, reach ~7% фолловеров) → урок: не доверяй одному инструменту — контрольный запрос дешевле паники; рост маленького аккаунта живёт не в постах, а в реплаях в нишу.

## Операционные предостережения на 02.10 (пятница)

1. **Приоритет очереди:** сначала Instagram-бриф (01.10, архив `CONTENT_BRIEF_instagram_20261001.md`), потом этот — если окно позволяет (пятница = 1 окно 09:00-12:00 UTC; 2 оригинала/день — потолок AuthorDiversityDecay). Если оба не влезают — этот бриф переносится на понедельник/вторник (НЕ выходные).
2. **Unanswered mentions:** TACTICS 01.10 фиксировал 2 непогашенных mention (UCP-тред 2105248101657387233, SkillSpector-тред 2105371192962195806) — закрыть до оригинала; реплаи требуют апрува текста Сергея → драфты Сергею, не автономно.
3. **Anti-dup перед постингом:** `operators/published_topic_check.py` + ручная кросс-проверка по published_posts.jsonl.
4. **Метрики:** Fo/Grok 35 imp — единственная слабая точка; при следующем оригинале <20 imp на 2 постах подряд → тормоз (пауза 48ч). По одной точке тактику не менять.
5. **После публикации:** 24h fetch, контрольная точка <20 imp → 🟡; 2 подряд <20 → пауза 48ч. Затем запросить свежий бриф у стратега.

## Deadline

**Черновик RU к:** 2026-10-02 09:00 UTC (или понедельник 09:00 UTC, если пятое окно пропущено)
**Публикация:** после approval Сергея (Human Gate)

## Резерв стратега (очередь на следующие прогоны)

1. **Ландшафт персональных агентов [BORDERLINE], score 31** — только новый угол Instinct ($1B raise при оценке $10B, 28.09 SiliconANGLE) + 2015-волна (Magic/Operator/Mezi). Fo-часть запрещена (FLOP). Факты: `research/personal-agents-landscape-2026-09-29.md`. Урок 23.09: war story с нашими цифрами, не рецепт.
2. **Muse trust layer** — RU готов (`drafts/muse_trust_layer_v1_ru.md`), нужен EN+MoA+обложка; новый бриф не требуется.
3. **Слепое ревью/filemap** — RU готов (`drafts/blind_review_filemap_v1_ru.md`), ждёт ok Сергея; новый бриф не требуется.
4. **Shopify WebMCP checkout hands-on** (TechCrunch 28.09) — WAIT: UCP DUP-7d до 06.10; вернуться после снятия DUP.

> Примечание о конкурсе 01.10 (23:30 UTC): победила robot-man shadowban/distribution — score 39 (свежесть 3×3=9; конкретность 3×3=9 — 10+ цифр; дуга 3×3=9; универсальность 2×2=4; контраст 2×3=6; разнообразие 2×1=2). Pre-gate «3 вопроса»: 3 «да». Instagram enforced-layer — не в конкурсе (забрифлен 01.10, score 34, не отработан — сохранён в архиве, приоритет очереди). Ландшафт агентов — 31 [BORDERLINE: дуга без нашего фикса + Fo-часть исчерпана FLOP-постом] — резерв. RAB9 — событие 24.09 (>72ч, свежесть 0) + крипто-контекст без цен-вето, но слабая дуга. GULAG — последняя запись 05.09 (26 дней); Alikhan — 11.09 (20 дней): оба вне окна. hermes-vault мета-файлы (SOUL-main/OPERATIONS/scorecard/Engineering Loop) — 0 коммитов за 7 дней. radar-scan — последний 01.09, 30 дней, STALE. Daily note 01.10 — пустая. Layer0 evac log — self-referential рутина, pre-gate отброс.

---

## Процесс robot-man

1. Прочитать этот брифинг + CONTENT_BRIEF_STANDARD.md
2. Прочитать AGENTS.md gates (robot-man) + CHRONOLOGY.md запись 29.09 + TACTICS.md 01.10
3. Anti-dup: `operators/published_topic_check.py` + ручная кросс-проверка по published_posts.jsonl
4. Написать драфт в голосе (VOICE_PROFILE.md + VOICE_LESSONS.md + ENGINEERING_POST_TEMPLATE.md)
5. RU-драфт → Сергей → ok → EN финал + обложка
6. MoA: deepseek-xai + viral-score + anti-ad
7. Факт-чек: каждая цифра ↔ таблица фактов (8 фактов выше)
8. Delivery Package → «ок/пости» → approval.token → post_with_log.sh + cover
9. CHRONOLOGY + 24h analytics

## 2026-10-02 — Cloudflare для агентов (пост 2105205... след.)
- >50% трафика сайтов на CF автоматический (Radar, заявление CF)
- Sandboxes GA (shell/ФС/процессы), Containers ~6x быстрее + снапшоты ФС, Workflows 50 000 concurrency / 300 creations
- Artifacts open beta (git-хранилище агентов), DO Facets (SQLite на AI-сборку), Vinext 1.0, Kitesurf (>730K WPT, WebMCP)
- Agent Memory managed, AI Search GA 01.10 (пиксели Qwen3-VL, OCR PDF, 10 MiB, биллинг 01.11, free tier), Browser Run (Live View, HITL, CDP, 4x)
- Monetization Gateway closed beta (HTTP 402, USDC/x402/Base, пер-request), Pay Per Use beta
- cf CLI ~3000 операций, Agent Lee, real-time issue detection → coding agent PR, Registrar API beta, Flagship, 8 observability апдейтов
- Безопасность: Mesh, non-human identities GA, Managed OAuth Access (RFC 9728), MCP governance, Threat Signals бесплатно
- Пасхалка: SKILL.md make-a-wish на birthday-week странице
- Модели 14+ провайдеров одним Workers-биндингом (Agents Week, inference layer)
