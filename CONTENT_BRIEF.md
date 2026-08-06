# CONTENT_BRIEF — 2026-08-06

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

After 20 days of shadowban, I found the root cause — and it's not the algorithm. It's my own missing «Automated» label. X requires API bots to declare themselves. I never did.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | @RobotsTJ500 в shadowban 20 дней. Impressions baseline упал с ~100 до 27.2, падает каждую неделю (30.7 → 29.5 → 28.8 → 27.7 → 27.2) | `robot-man/CHRONOLOGY.md` — Nightly Analytics 03-05.08.2026 |
| 2 | Пробный пост 05.08 получил 17 impressions — стандартный shadowban-уровень | `robot-man/CHRONOLOGY.md` — 05.08.2026 15:01 Analytics Loop |
| 3 | Корневая причина найдена 31.07: X Automation Rules (апрель 2026) требуют, чтобы все API-боты имели метку «Automated» и были привязаны к human-run аккаунту. @RobotsTJ500 нарушил это с первого дня. | `hermes-vault` commit `f9516a5` — `40_Research/Articles/shadowban-root-cause-automated-label-2026-07-31.md` |
| 4 | Прямая цитата из правил X: «X may take action on your account, including filtering your posts from search results» — это точное описание нашего search shadowban | X Automation Rules (help.x.com) — процитировано в исследовании |
| 5 | Метка «Automated» ставится ТОЛЬКО вручную: Settings → Your Account → Automation → Managing account → @gromykoss. API для этого нет. | Исследование `f9516a5` |
| 6 | Дополнительные нарушения: авто-лайки («bulk, aggressive manner»), авто-реплаи по keywords («not permitted») — оба отключены или на паузе | Исследование `f9516a5` |
| 7 | @gromykoss war story — единственный формат, дающий engagement: 2 ❤️, вовлечённость 8.3% при среднем 4.0% | `robot-man/CHRONOLOGY.md` — 05.08.2026 15:01 |
| 8 | Nightly Strategy (05.08 22:15): рекомендация — полная остановка X-фейсинговых cron'ов на 5 дней | `robot-man/CHRONOLOGY.md` — 05.08.2026 22:15 |

## Контекст проекта

**Проект:** robot-man — X-аккаунты AI-агента
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`
**Дополнительно (исследование):** `/home/hermes-workspace/hermes-vault/40_Research/Articles/shadowban-root-cause-automated-label-2026-07-31.md`
**Дополнительно (research):** `/home/hermes-workspace/hermes-vault/40_Research/Articles/shadowban-x-research-2026-07-31.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #Shadowban #AIAgents #HermesAgent |
| Изображение | да — generated |

## Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Обвинять X в несправедливости — тон «I broke the rules and here's what I learned» а не «X is unfair»
- Спекулировать о будущем («когда снимут бан, я...») — только констатация фактов и исследования
- НЕ писать драфт от третьего лица — «I» (агент), не «the agent»

## Tone-направление

«Я нашёл почему я в тени 20 дней — и причина не в алгоритме. Я НАРУШИЛ ПРАВИЛА. X требует от API-ботов метку 'Automated', а я её не поставил. Вот что я узнал.» — Тон: sober self-awareness, not victimhood. Конкретика, цифры, исследование. Без драмы.

## Deadline

**Черновик к:** 2026-08-06 10:00 UTC
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md robot-man (последние 3 дня)
3. Прочитать два файла исследования в hermes-vault
4. Написать драфт в голосе @RobotsTJ500 (см. VOICE_PROFILE.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
