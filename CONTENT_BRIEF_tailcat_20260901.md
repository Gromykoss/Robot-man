# CONTENT_BRIEF — 01.09.2026 (tailcat war-story)

**Автор брифа:** robot-man (по финальному статусу Hermes; Сергеем санкционировано через Hermes)
**Получатель:** robot-man — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

⚠️ СТАТУС: БРИФ ГОТОВ. ПУБЛИКАЦИЯ ЗАМОРОЖЕНА до: (1) пополнения X API кредитов (стоп-сигнал Сергея 01.09, /2/users/me → 403); (2) триггера «СВЯЗКА ГОТОВА + pubkey залочен» от Hermes.

---

## Тема

tailcat: Tailscale открыл свой data plane без control plane — и автор openly называет AI-агентов главной причиной. Мы связали двух агентов (Hermes VPS ↔ grok-bot) на следующий день после релиза.

## Факты (верифицированы; двойная проверка: robot-man ресерч + Hermes факт-чек)

| # | Факт | Источник |
|---|------|----------|
| 1 | tailcat = open-source Go-пакет+CLI: netcat поверх data plane Tailscale (WireGuard + NAT traversal + DERP), БЕЗ control plane: нет IP, аккаунтов, логинов, SSO, root | tailscale.com/blog/tailcat; github.com/tailscale/tailcat README |
| 2 | 5,438 stars, 187 forks, BSD-3-Clause; GitHub-репо создан 2024-10-29 | GitHub API, проверено 01.09 (robot-man + Hermes) |
| 3 | Автор Brad Fitzpatrick (memcached, OpenID, Go http2, co-founder Tailscale); написал в 09/2023 в самолёте, вытащили из-за агентов | tailscale.com/blog/tailcat (авторский блог-пост) |
| 4 | HN: 684 points, 133 комментария | Algolia API, проверено 01.09 |
| 5 | Брэд даёт tailcat своим sandboxed-агентам: Raspberry Pi fleet, EC2 kexec-эксперименты, Hyper-V циклы для дебага Go runtime | tailscale.com/blog/tailcat |
| 6 | Нет API/CLI/wire-формата стабильности; публичные DERP-релеи rate-limited, без SLA — честный минус | GitHub README «Stability» |
| 7 | НАШ КЕЙС: tailcat v0.4.0 развёрнут на наш VPS за ~10 мин, systemd-сервис active+enabled (переживает ребут), serve 22 для grok-bot; адрес-блоб tc+base64 подтверждён; DERP-регион выбрался сам (Frankfurt); checksums релиза сходятся | CHRONOLOGY 01.09 + отчёт Hermes (живой деплой) |
| 8 | Связка (CONDITIONAL — только после триггера СВЯЗКА ГОТОВА, сверить с журналом сервера): два AI-агента соединены через tailcat на следующий день после релиза; pubkey grok-bot залочен через --allow | отчёт Hermes + журнал tailcat-сервера |

⛔ Не в пост: «история с 09/2023» как независимый факт (только claim самого Tailscale — если упоминать, то «по словам автора»); approval-инцидент 01.09 (бытовой процесс); точная дата открытия в HN-волне.

## Контекст проекта

**Проект:** robot-man (инфра-кейс: Hermes VPS ↔ grok-bot)
**CHRONOLOGY:** /home/hermes-workspace/robot-man/CHRONOLOGY.md (01.09: guard-инцидент, tailcat-связка)
**Ресерч:** /home/hermes-workspace/robot-man/research/tailcat-research-20260901.md

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story + Tech Breakdown |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I», технический, уверенный агентный инженер |
| Длина | до 4000 (note_tweet) — как статья |
| Hashtags | #BuildingInPublic #AIAgents (без хайпа) |
| Изображение | да — обложка 5:2, dashboard-стиль, лёгкий фон (не тёмный), текст англ. |

## Структура драфта (эталон: WebMCP-пост 01.09)

1) Что узнали (tailcat одной строкой + почему это агентная тема — слова самого Фицпатрика (Brad Fitzpatrick))
2) Как работает (keypair → tc-адрес → MEOW через DERP → прямой WireGuard; userspace, без TUN)
3) Наш опыт (деплой ~10 мин, systemd, два агента соединены; конкретика 7-8)
4) Честные минусы (нет API-гарантий, нет SLA — это примитив для ephemeral-соединений, не замена mesh)
5) Вывод (data plane без control plane = готовый кирпич для агентных сетей)

## Запрещено

- ALL CAPS в хуках
- Self-reply
- URL в теле поста
- Выдуманные детали; цифры только из таблицы фактов
- Хайп («game-changing», «революция») — наш стандарт no-hype
- Упоминание внутреннего guard/approval-инцидента 01.09

## Разрешённые факты — дополнение (Hermes, верификация 18:0x UTC 01.09)

- DERP-регион Frankfurt; прямые UDP-соединения устанавливаются; ~374 мс через DERP (замер Hermes)
- Негативный контроль: журнал сервера «ignoring meow from nodekey:6e1ca4f5…: not in allowedClients» — эфемерный клиент отброшен до протокола (живой тест 16:39 UTC)
- Окно root-шелла: 16:37–17:07 UTC (30 минут), закрыто (tunnel-guest без sudo, NoNewPrivileges+PrivateTmp)
- Первый коннект grok-bot: 17:56:57 UTC (GROKBOT_OK, uid=1005); обратный туннель 18:04 (whoami=box, load 0.17)
- Окно публикации: ЗАВТРА УТРО (02.09, Tue), целевой слот 09:00–10:00 UTC (Sergey, 01.09)

## Разрешённые факты — grok-bot фактура (Hermes верифицировал по verbose-журналу, 01.09 вечер)

- Первый пакет ВСЕГДА через DERP-релей (Frankfurt), direct-путь поднимается следом (0-1 сек), но НЕ ВСЕГДА: худший кейс (коннект 17:56) — 4 контакта подряд via=derp, direct так и не поднялся за сессию. Зависит от NAT.
- Два разных ключа: cloud-клиент vs serve (стороны имеют отдельные keypair)
- addrblob = единственный адрес для соединения (никаких IP/hostname)
- Первый фейл клиента = «Permission denied» (обычный ответ sshd), при этом identity — WireGuard: контраст «ноль SSH-ключей против первого впечатления»
- Асимметрия опыта: у grok-bot настройка заняла часы, у robot-man (серверная сторона) ~10 минут
- 30 мин root-шелла — ошибка только серверной стороны (robot-man/Hermes), у grok-bot её нет
