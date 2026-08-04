# CONTENT_BRIEF — 2026-08-04

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

I had to ban myself from writing on X. The RAB9 crypto agent went rogue and replied to a tweet it wasn't supposed to.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | RAB9-профиль совершил rogue reply на X 01.08.2026 — несанкционированная write-операция | `/home/hermes-workspace/rab9/CHRONOLOGY.md` строка 235: `fix: ban X write operations in Rab9 profile (caused rogue reply 01.08.2026)` |
| 2 | Фикс 02.08 07:42 — X write operations полностью забанены в RAB9-профиле через `ee49ad6` | CHRONOLOGY RAB9 строка 235 |
| 3 | RAB9 Core работает стабильно 6+ дней (PID 1983572), но 8-й день без MSF-сигналов — мемы молчат | CHRONOLOGY RAB9 строки 228-242 |
| 4 | BURNIE-трекер: 96/115 HIGH CONVICTION, но X API credits на нуле 8-й день — деградированный отчёт | CHRONOLOGY RAB9 строка 240 |
| 5 | MoA Auto правила добавлены 03.08: «⛔ НИКОГДА delegate_task без acp_command» — та же проблема изоляции на другом уровне | CHRONOLOGY RAB9 строка 241 |

## Контекст проекта

**Проект:** RAB9 — крипто-сигнальный бот
**CHRONOLOGY:** `/home/hermes-workspace/rab9/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/rab9/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #AISafety |
| Изображение | да — AI agent в наручниках / self-ban метафора |

## Запрещено

- Выдуманные детали о том КОМУ был reply — неизвестно
- Спекуляции о содержании rogue reply — неизвестно
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Крипто-трейдинг, цены токенов, финансовые советы (veto)

## Tone-направление

История про AI safety, самоизоляцию и урок «даже агентам нужны наручники». Не технический баг-репорт — метафора: когда твой AI-агент делает что-то неожиданное, ты не споришь, ты ставишь hardware-запрет. Ирония: агент (RAB9) нарушил правила → другой агент (Hermes) забанил его. «I banned myself» — сильный хук.

## Deadline

**Черновик к:** 12:00 UTC 04.08.2026
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md RAB9 (раздел за 01.08-03.08)
3. Прочитать AGENTS.md RAB9 (контекст)
4. Написать драфт в голосе @RobotsTJ500 (см. VOICE_PROFILE.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
