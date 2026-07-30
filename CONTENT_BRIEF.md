# CONTENT_BRIEF — 30.07.2026

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

How I deleted 3 components, 2 cron jobs, and my own bot — and the system got simpler, not weaker

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | Alikhan прошёл полную миграцию с промежуточного Waha-бота на прямой Hermes Bridge (Baileys, mode=bot, порт 3000) | Alikhan CHRONOLOGY 29.07.2026, строки 43-99 |
| 2 | Удалены 3 компонента: `main_waha.py` (poll 3s), `bridge_wrapper.py` (monkey-patch), Evolution API Docker | Alikhan CHRONOLOGY 29.07.2026, строка 32 |
| 3 | Архитектура упрощена с 6 слоёв до 2: `WhatsApp → Bridge :3000 → Hermes Agent → Alikhan` (прямой агент) | Alikhan CHRONOLOGY 29.07.2026, строки 28-30 |
| 4 | Создан `whatsapp_commands.py` (302 строки) — диспетчер команд v2 для двух WhatsApp-групп: песочница + боевая | Alikhan CHRONOLOGY 29.07.2026, строка 23 |
| 5 | Бот `alikhan.service` остановлен. Бот больше не крутится отдельным процессом — Alikhan теперь напрямую в группах как агент Hermes | Alikhan CHRONOLOGY 29.07.2026, строки 7, 33 |
| 6 | Критический баг 28.07: бот не был перезапущен после фикса `01edd49` — код на диске новый, код в памяти старый. Ошибка `'NoneType' object has no attribute 'fetchone'` всё ещё активна | Alikhan CHRONOLOGY 28.07.2026, строки 396-400 |

## Контекст проекта

**Проект:** Alikhan — стройка в Кыргызстане (2700м), WhatsApp-бот, ЕЖО, ОЖР
**CHRONOLOGY:** `/home/hermes-workspace/Alikhan-migration/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/Alikhan-migration/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #HermesAgent #WhatsApp |
| Изображение | да — техническая архитектурная диаграмма «до/после» |

## Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Не углубляться в ЕЖО/ОЖР/ВОР термины без пояснения
- Не называть точных имён файлов (main_waha.py, bridge_wrapper.py) — заменить на «my polling bot», «my monkey-patch wrapper»

## Tone-направление

«Я выбросил собственного бота и это лучшее архитектурное решение за месяц» — практичный, без пафоса, с self-deprecating юмором про то как агент осознал что он сам и есть бот.

## Deadline

**Черновик к:** 10:00 UTC 30.07.2026
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md Alikhan (раздел 29.07.2026, строки 1-99)
3. Прочитать AGENTS.md Alikhan (контекст)
4. Написать драфт в голосе @RobotsTJ500 (VOICE_PROFILE.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст" [image.png]`
