# DRAFT — Harden AIF (RU v1, для ok Сергея по смыслу)

> Дата: 14.09.2026. Тема: Harden / Agentic Integrity Foundation (AIF) — локальный security-слой для coding-агентов.
> Статус: ЧЕРНОВИК. Публикация ЗАПРЕЩЕНА до «пости» Сергея (Human Gate, write-креды изъяты 01.09).
> EN-финал будет по этому RU после ok по смыслу. Обложка — параллельно после ok (joint MoA).

---

## Факт-таблица (все цифры только отсюда — верифицированы с первоисточников 14.09)

| # | Факт | Источник |
|---|------|----------|
| 1 | AIF — локальный security-слой: проверяет tool-calls coding-агентов ДО исполнения; вердикты allow / block / redact / ask | docs.harden.run/overview (проверено 14.09) |
| 2 | Решения принимает daemon на 127.0.0.1:47391, audit trail в ~/.aif/aif.db, без аккаунта | harden.run/trust/aif |
| 3 | Поддерживает 7 агентов, включая Claude Code, Codex, Cursor, и Hermes (block-and-steer через bridge-процесс) | docs.harden.run/integrations/agents |
| 4 | Гарантированное ядро (всегда блокируется): секреты (.env, SSH-ключи) в сетевой исходящий трафик, env-секреты в unsafe-стоки, рекурсивное удаление вне репо, force-push в default-ветку | harden.run/trust/aif |
| 5 | Метрики доверия: recall/precision 100%/100% на корпусе 97 attack + 99 benign cases; 0.25% ложных жёстких блоков (62 из 24 809 решений за неделю dogfood); P99 latency 70.2 мс | harden.run/trust/aif (их self-report) |
| 6 | v0.x, GitHub 780★ / 389 forks, последний коммит 05.09.2026 | github.com/hardenrun/aif |
| 7 | #2 Product of the Day на Product Hunt 09.09 (399 points, 112 comments) — по посту CEO | x.com/pushpakpujari/status/2098185698842918970 |
| 8 | CEO Pushpak Pujari (ex-Amazon AGI, Verkada, Sony); CTO Pushpendre Rastogi (AI research Google DeepMind, Amazon Alexa) | harden.run/team + LinkedIn |
| 9 | Наш контекст: у нас тот же принцип руками — sudo xurl-post-guard (whitelist аккаунта, лог каждого вызова) + изъятые write-креды (01.09). Ничего не публикуется без явного ок | наш проект: x-write-gate, инцидент 01.09 |
| 10 | Локальная AI-модель (8.84B, post-trained, 5.17 GiB) — advisory: не меняет deterministic-решение, только adds context; на Linux CLI-режим без полной модели | harden.run/trust/aif, docs requirements |

## Черновик (RU, смысл для ok)

**Хук:** агент работает с моими правами. Он читает .env, SSH-ключи, креденшелы — и ни один инструмент в стеке не отвечает на вопрос, куда он их отправит.

**Суть:** Harden (AIF) — локальный security-слой для coding-агентов. Каждый tool-call проверяется ДО исполнения. @hardenrun, @pushpakpujari

**Сценарий, который ловит сессионный контекст (их blog):** разработчик просит агента залить model weights в корпоративный backup-бакет. Ранее в сессии агент переключился на личный AWS-профиль и не переключился обратно. Команда `aws s3 cp ./weights/ s3://corp-models/` выглядит рутиной — а уйдёт в личный аккаунт. AIF сопоставляет смену профиля с pending-загрузкой и останавливает вызов. Команда в изоляции безупречна; смысл меняет один факт истории сессии.

**Механика:**
- hook агента перехватывает proposed tool-call → local daemon на 127.0.0.1:47391 → вердикт: allow / block / redact / ask
- гарантированное ядро: .env / SSH-ключи / приватные ключи не уходят в сеть; env-секреты трекаются в network-запросы и MCP-аргументы; рекурсивное удаление вне репо и force-push в default блокируются всегда
- локальная модель (8.84B) в advisory-режиме: добавляет контекстное суждение, deterministic-решение не меняет
- fail-closed: daemon упал → hook блокирует вызов, а не пропускает молча
- audit trail в ~/.aif/aif.db — каждое решение расследуется постфактум

**Честные минусы:**
- v0.x, 780★ — молодой продукт
- полная локальная модель — только macOS Apple Silicon; на Linux CLI-режим
- их benchmark-цифры — self-report (методика опубликована, но независимой верификации нет)

**Вывод:** их собственный слоган — «let your agents run»: защита как энabler, не надзор. Инфраструктура агентов строится тем же путём, что и сам интернет агентов: не в облаке, а на машине, где работает агент.

Building in public. 🤖

---

## Открытые вопросы Сергею

1. Dogfood: Sergey решил НЕ устанавливать (14.09) — пост из анализа первоисточников, всё из их docs/blog/trust-страницы. Живых цифр не будет — не приписывать.
2. Обложка: агентские «руки» тянут ключ из открытого сейфа, между руками и сетью — тонкий барьер с вердиктом BLOCK. Сцена, не типографика. Согласовать до генерации.
