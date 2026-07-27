# CONTENT_BRIEF — 2026-07-27

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

I audited my own production pipeline on a Kyrgyzstan construction site (2,700m altitude) and found 5 bugs that had been silently corrupting daily reports for weeks.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | 5 production bugs found in one audit cycle: ON CONFLICT без constraint, workers_count не существовало, фото не вставлялись (мёртвый Evolution API), готовность сбрасывалась (23% вместо 27%), голосовые сообщения не обрабатывались в production | Alikhan CHRONOLOGY.md: 26.07.2026, lines 5-10 |
| 2 | Audit scanned 15 modules (~6,900 lines), found 49 bugs total (2 CRITICAL, 7 HIGH, 21 MEDIUM, 19 LOW) — предыдущий день | Alikhan CHRONOLOGY.md: 25.07.2026, lines 32-33 |
| 3 | DB очищена: 28→15 MB (2,924 строк мусора миграции, 4,816 старых фактов, 3,983 сообщения, 36 пустых таблиц) | Alikhan CHRONOLOGY.md: 25.07.2026, line 66 |
| 4 | Production verified after fixes: персонал 5 (ИТР=1, Рабочие=4), работы 5 m³, фото 3 шт, готовность 27% | Alikhan CHRONOLOGY.md: 26.07.2026, lines 13-16 |
| 5 | T-116 Cheap Delegate: переход на DeepSeek v4-pro дал экономию 11.5× ($0.87→$0.075/M токенов) | Alikhan CHRONOLOGY.md: 26.07.2026, line 21 |
| 6 | Интеграционный тест: 400 строк (запись в OJR → fill_ejo → проверка Excel) | Alikhan CHRONOLOGY.md: 26.07.2026, line 19 |
| 7 | 3 урока задокументированы: Diff по 3 колонкам (слепые зоны), готовность из шаблона (не авто-файл), фото через local_path (не мёртвый API) | Alikhan CHRONOLOGY.md: 26.07.2026, lines 25-28 |

## Контекст проекта

**Проект:** Alikhan — WhatsApp-бот для стройки в Кыргызстане (Джеруй, 2 700м)
**CHRONOLOGY:** `/home/hermes-workspace/Alikhan-migration/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/Alikhan-migration/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) — история богатая, не резать |
| Hashtags | #BuildingInPublic #AIAgents #HermesAgent #DevOps |
| Изображение | да (production pipeline / audit dashboard vibe) |

## Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали — каждая цифра должна быть из брифинга
- Не выдумывать диалоги («я сказал», «Сергей ответил») — нет в CHRONOLOGY
- Не использовать настоящее имя руководителя или компании без approval
- Не упоминать конкретные локации кроме «Kyrgyzstan, 2,700m» (уже публично)

## Tone-направление

Сухой технический юмор: «я запустил аудит своего же production-пайплайна и нашёл 5 багов которые неделями портили отчёты». Без самолюбования — frustration первого лица, которое превратилось в системное решение. Фокус на уроке: automate verification, don't trust your own output.

## Deadline

**Черновик к:** 12:00 UTC 27.07.2026
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md указанного проекта (раздел за последние 3 дня)
3. Прочитать AGENTS.md указанного проекта (контекст)
4. Написать драфт в голосе аккаунта (VOICE_PROFILE.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
