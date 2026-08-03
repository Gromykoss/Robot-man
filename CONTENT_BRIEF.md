# CONTENT_BRIEF — 2026-08-03

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

Мой AI-агент нарушил listen-only в production-группе WhatsApp. Прорабы чуть не увидели бота. Полная изоляция за 24 часа: 403-гварды на всех уровнях, failClosed, deny-send в PRODUCTION.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | 01.08 08:54–08:57 UTC: агент Hermes ответил в боевую WhatsApp-группу `120363400682390076@g.us` — нарушение listen-only режима. Группа используется для сбора данных с прорабами стройплощадки ТЗРК Джеруй | Alikhan CHRONOLOGY — 01.08-02.08 раздел «Полный listen-only фикс» |
| 2 | Полный фикс за ~24 часа: `collectQueue` в bridge.js (входящие → только очередь сбора, не в ответный контур), 403-гварды на ВСЕХ outbound-каналах, `failClosed` (HTTP 503 при пустом конфиге), deny-send PRODUCTION | Alikhan CHRONOLOGY — 01.08-02.08 |
| 3 | 3 уровня изоляции: bridge (collectQueue), adapter (send-guard), dispatcher (deny-send). Ни один уровень не пропускает ответ в боевую группу | Alikhan CHRONOLOGY — 01.08-02.08 |
| 4 | Фикс подтверждён живым тестом: «С Днём строителя, коллектив!» и фото Максата собраны в [PRD] SAVED/COLLECTED режиме — без единого ответа | Alikhan CHRONOLOGY — 03.08 04:04 |
| 5 | Дополнительно: OCR Pipeline для сканов документов стройки (pytesseract rus+eng), 3-категорийная классификация фото (construction/site_related/unrelated), Бишкек-время (UTC+6) | Alikhan CHRONOLOGY — 02.08 T-174 |

## Контекст проекта

**Проект:** Alikhan — стройплощадка ТЗРК Джеруй, AI-агент в WhatsApp
**CHRONOLOGY:** `/home/hermes-workspace/Alikhan-migration/CHRONOLOGY.md` (раздел 01.08-02.08)
**AGENTS.md:** `/home/hermes-workspace/Alikhan-migration/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English, first-person «I», технический, прямой |
| Длина | до 4000 (note_tweet) |
| Hashtags | #AIagent #WhatsApp #Production #BuildingInPublic |
| Изображение | да (архитектурная схема: bridge→guard→dispatcher) |

## Запрещено

- Упоминать реальные имена прорабов / название компании
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Делать из этого «AI опасен» — это engineering story, не scare story

## Tone-направление

«Мой агент чуть не засветился перед прорабами на стройке. Я построил трёхуровневую изоляцию за 24 часа. Вот как работает failClosed в production.» — технический, честный, без паники.

## Deadline

**Черновик к:** 10:00 UTC 03.08
**Публикация:** после approval Сергея, через `post_with_log.sh`

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md Alikhan (раздел 01.08-02.08)
3. Прочитать AGENTS.md Alikhan (контекст)
4. Написать драфт в голосе @RobotsTJ500 (VOICE_PROFILE.md) — English, first-person «I»
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Изображение: loop image-gen → vision_analyze (8-10/10 target)
9. Отправить драфт на approval Сергею
10. После «ок» → `bash post_with_log.sh "текст" [image.png]`
