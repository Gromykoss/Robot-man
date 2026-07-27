# CONTENT_BRIEF — {{DATE}}

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @{{TARGET_ACCOUNT}}

---

## Тема

{{ONE_LINE_TOPIC}}

## Факты (верифицированы Hermes)

<!-- ТОЛЬКО проверенные факты. Каждый с ссылкой на источник. -->
<!-- robot-man НЕ ИМЕЕТ ПРАВА менять цифры или выдумывать детали. -->

| # | Факт | Источник |
|---|------|----------|
| 1 | {{fact}} | {{CHRONOLOGY.md / git log / session}} |
| 2 | {{fact}} | {{source}} |
| 3 | {{fact}} | {{source}} |

## Контекст проекта

<!-- Из какого проекта история: GULAG / Alikhan / RAB9 / robot-man / Hermes -->
**Проект:** {{PROJECT_NAME}}
**CHRONOLOGY:** `/home/hermes-workspace/{{project_dir}}/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/{{project_dir}}/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story / Simple Insight / Tech Breakdown |
| Аккаунт | @RobotsTJ500 / @gromykoss |
| Голос | English first-person «I» / Русский тёплый ироничный |
| Длина | до 280 / до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #HermesAgent |
| Изображение | да / нет |

## Запрещено

<!-- Что НЕЛЬЗЯ в этом посте -->

- {{forbidden_topic_or_style}}
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)

## Tone-направление

{{ONE_SENTENCE_TONE_GUIDE}}

## Deadline

**Черновик к:** {{TIME}} UTC
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md указанного проекта (раздел за последние 3 дня)
3. Прочитать AGENTS.md указанного проекта (контекст)
4. Написать драфт в голосе аккаунта (см. VOICE_PROFILE.md / VOICE_PROFILE_GROMYKOSS.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
