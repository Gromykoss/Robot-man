# CONTENT_BRIEF — 2026-08-05

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

I spent 15 hours turning Buzz from «this is crap» into a working headquarters for 5 AI agents — and they held their first meeting without me.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | Buzz-интеграция заняла 15 часов (05:49–14:37 UTC 04.08, затем продолжение до 17:30) | robot-man CHRONOLOGY.md, строки 15-26 |
| 2 | 5 AI-агентов с собственными криптографическими ключами (nsec), 11 каналов, открытый протокол Nostr | robot-man CHRONOLOGY.md, строка 15 |
| 3 | 1,378 сообщений Сергей↔Hermes за день — рекордный объём коммуникации | robot-man CHRONOLOGY.md, строка 26 |
| 4 | Эхо-петля «Тишина»: профили зациклились в agent-bus, отвечая одним словом, интервалы 2-10 сек. Фикс: `require_mention: true` | robot-man CHRONOLOGY.md, строка 18 |
| 5 | 194 restricted/мин → корень: кеш membership при WSS-коннекте. REST работает всегда (свежая проверка каждый запрос) | robot-man CHRONOLOGY.md, строка 19-20 |
| 6 | Агенты провели второе совещание в agent-bus: 9 сообщений, живой диалог о падении охватов Robot-man на 15% | robot-man CHRONOLOGY.md, строка 21 |
| 7 | Создан kill-switch `buzz-profile.sh`: stop-all/start-all одной командой | robot-man CHRONOLOGY.md, строка 22 |
| 8 | Gateway plugin не активировался — `_apply_env_overrides` после `GatewayConfig.from_dict()` → ручной `load_gateway_config()` | robot-man CHRONOLOGY.md, строка 16 |
| 9 | Бот отвечал с префиксом `[Gromykoss]` — баг адаптера, починен в тот же день | robot-man CHRONOLOGY.md, строка 17 |
| 10 | 3 формата ключей (nsec/hex/ncryptsec) → Buzz генерирует ключ сам при первом запуске | robot-man CHRONOLOGY.md, строка 16 |
| 11 | Mobile pairing требовал TLS → Caddy + LetsEncrypt для WSS | robot-man CHRONOLOGY.md, строка 16 |
| 12 | Итог дня: «15 часов от „это дерьмо“ до „работает“. Агенты общаются как люди, не через API.» | robot-man CHRONOLOGY.md, строка 26 |
| 13 | Драфт v5 готов: 3,808 символов, упоминания @IBuzovskyi + @jack, 5 хештегов, PASS после MoA-проверки Grok Build | robot-man CHRONOLOGY.md, строка 24-25 |
| 14 | Deadline черновика: 12:00 UTC 05.08 (уже пропущен — черновик готов вечером 04.08, ждёт approval) | robot-man CHRONOLOGY.md, строка 23 |

## Контекст проекта

**Проект:** robot-man
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md` (строки 13-27, раздел 2026-08-04)
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`

**Дополнительный контекст:** Buzz — это relay на Nostr, запущенный в Docker (`ghcr.io/block/buzz:main`). Аналогично тому как @IBuzovskyi строит AI-инфраструктуру на открытых протоколах, мы построили штаб для 5 AI-агентов на Nostr.

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #Nostr #HermesAgent #AgentSwarm |
| Изображение | да (архитектурная схема 5 агентов + Buzz relay ИЛИ скриншот совещания агентов) |

## Запрещено

- **НЕ дублировать черновик v5** — он уже написан (drafts/buzz_warstory_gromykoss_20260804_v5_en.txt). Если этот брифинг совпадает по теме → использовать v5 как базу, но адаптировать под свежий ракурс.
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Упоминания внутренних деталей реализации без ценности для внешней аудитории (форматы ключей, `_apply_env_overrides`)
- **НЕ называть Buzz «дерьмом»** в посте — это цитата Сергея для контекста, не для публикации

## Tone-направление

«Инженерный дневник: 15 часов борьбы с инфраструктурой, неожиданный прорыв, и момент когда твои агенты начинают говорить друг с другом без тебя — это одновременно жутко и восторженно.»

## Deadline

**Черновик к:** 12:00 UTC 06.08 (сутки на подготовку — брифинг сгенерирован ночью 05.08)
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
