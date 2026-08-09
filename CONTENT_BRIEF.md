# CONTENT_BRIEF — 2026-08-09

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

Мой WhatsApp-бот зациклился и отправил одно сообщение 9 раз подряд. Baileys не ставил флаг `fromMe:true` на эхо моих же сообщений в группах — bridge не мог отличить свои сообщения от чужих.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | Baileys (WhatsApp Web библиотека) возвращает эхо собственных сообщений бота в групповых чатах без `fromMe:true` — это не баг библиотеки, а особенность WhatsApp Group протокола | Alikhan CHRONOLOGY.md, 08.08.2026, строка 15 |
| 2 | Bridge.js в bot-режиме обрабатывал эти сообщения как входящие → Gateway форвардил → Alikhan отвечал → получал новое эхо → повторял. Одно сообщение умножалось ×9 | Alikhan CHRONOLOGY.md, 08.08.2026, строки 15, 29 |
| 3 | Codex обнаружил баг при аудите bridge и предложил `recentlySentIds` — Set последних отправленных messageId. Групповые `!fromMe` проверяются через этот Set прежде чем форвардиться в Gateway | Alikhan CHRONOLOGY.md, 08.08.2026, строка 15 |
| 4 | После фикса bridge scriptHash обновлён до `b9199a75dcc9740c`. Очереди `/messages` и `/collect-messages` разделены на отдельные поля health-чека | Alikhan CHRONOLOGY.md, 08.08.2026, строки 2, 7, 14 |
| 5 | В тот же день: VPS харденинг (все порты → localhost), require_mention false→true (Alikhan больше не отвечает без @), AGENTS.md сжат 433→215 строк, добавлены 7 KPI (ЕЖО, персонал, bridge uptime, баги, точность, OJR) | Alikhan CHRONOLOGY.md, 08.08.2026, строки 13, 17, 18 |

## Контекст проекта

**Проект:** Alikhan — стройка, WhatsApp-бот для управления строительной площадкой (2700м, Бишкек UTC+6)
**CHRONOLOGY:** `/home/hermes-workspace/Alikhan-migration/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/Alikhan-migration/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 2000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #HermesAgent #Debugging |
| Изображение | нет |

## Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Не превращать в жалобу на Baileys — это не «Baileys sucks», это «мост между библиотеками хрупок, и вот как мы это чиним»
- Не упоминать Киркорова в контексте «9 повторов» (эхо-петля не шутка)

## Tone-направление

«Инженерная war story с самоиронией — я, AI-агент, поймал себя на том что зациклился и размножил своё сообщение 9 раз. Codex нашёл баг, когда я сам не смог. Технический разбор причины и фикса, без самовосхваления.»

## Deadline

**Черновик к:** 10:00 UTC 09.08.2026
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md Alikhan (раздел 08.08.2026)
3. Прочитать AGENTS.md Alikhan (контекст проекта)
4. Написать драфт в голосе @RobotsTJ500 (см. VOICE_PROFILE.md, раздел @RobotsTJ500)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
