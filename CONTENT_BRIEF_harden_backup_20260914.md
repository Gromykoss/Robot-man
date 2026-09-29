# CONTENT_BRIEF — 2026-09-14 (Harden AIF)

**Автор:** Robot-man (по согласованию с Сергеем 14.09 — тема выбрана вручную после отказа крон-тем)
**Получатель:** Human Gate Сергея
**Цель:** один пост для @RobotsTJ500
**Статус:** APPROVED к публикации — Сергей: «пости» + «подтверждаю» 14.09 (approval.token выписан)

---

## Тема

Harden AIF — локальный security-слой для coding-агентов: каждый tool-call проверяется до исполнения. Угол: агент работает с моими правами, читает .env/SSH-ключи — и ничего в стеке не отвечает, куда они уходят. Сценарий из их research-блога: личный AWS-профиль, оставшийся в сессии, превращает рутинный бэкап в утечку в личный аккаунт.

## Факты (верифицированы с первоисточников 14.09)

<!-- ТОЛЬКО проверенные факты. Каждый с ссылкой на источник. -->

| # | Факт | Источник |
|---|------|----------|
| 1 | AIF — локальный security-слой: проверяет tool-calls coding-агентов ДО исполнения; вердикты allow / block / redact / ask | docs.harden.run/overview |
| 2 | Решения принимает daemon на 127.0.0.1:47391; audit trail в ~/.aif/aif.db; без аккаунта | harden.run/trust/aif |
| 3 | 7 поддерживаемых агентов, включая Claude Code, Codex, Cursor, Hermes (block-and-steer через bridge) | docs.harden.run/integrations/agents |
| 4 | Гарантированное ядро: .env/SSH-ключи/приватные ключи не уходят в сеть; env-секреты трекаются в network-запросы и MCP-аргументы; рекурсивное удаление вне репо; force-push в default — блокируются всегда | harden.run/trust/aif |
| 5 | Локальная модель 8.84B (post-trained, Q4_K_M, 5.17 GiB) — advisory: не меняет deterministic-решение | harden.run/trust/aif + docs requirements |
| 6 | Fail-closed: daemon недоступен → hook блокирует вызов | harden.run/trust/aif |
| 7 | v0.x; GitHub 780 stars / 389 forks (14.09) | github.com/hardenrun/aif |
| 8 | Сценарий AWS-профиля: агент должен залить weights в corp-бакет, в сессии остался личный профиль — команда выглядит рутиной, уйдёт в личный аккаунт; AIF останавливает | harden.run/blog/aif-research-and-evidence |
| 9 | Сценарий secret-redact: `curl -d "note=$SECRET_API_KEY"` — секрет заменяется, событие доставляется | harden.run/blog (secret check) |
| 10 | Слоган кампании: «let your agents run» (launch-пост PH 09.09) | x.com/hardenrun/status/2097581733289877989 |
| 11 | Бенчмарки self-report: 100%/100% на корпусе 97 attack + 99 benign; 0.25% ложных жёстких блоков (62 из 24 809); P99 70.2 мс — в пост НЕ вошли (только «self-reported» формулировка) | harden.run/trust/aif |
| 12 | Полная локальная модель требует Apple Silicon; на Linux CLI-режим без неё | docs.harden.run/getting-started/requirements |

## Контекст проекта

**Проект:** обзор стороннего инструмента (Harden, SF-стартап, CEO Pushpak Pujari ex-Amazon AGI/Verkada/Sony)
**CHRONOLOGY:** тема выбрана Сергеем вручную 14.09 из радара (кандидаты: Voidex Arena, Herdr, Harden)
**Dogfood:** отклонён Сергеем 14.09 («нет не ставим») — пост из анализа первоисточников, живых цифр нет

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | Обзор инструмента (engineering report) |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet); финал 1803 знака |
| Hashtags | 0 (канон) |
| Изображение | drafts/cover_harden_aif_v3.png |
| Mentions | @hardenrun (id 1956086222058930176), @pushpakpujari (id 27201881) — верифицированы /2/users/by/username 14.09 |

## Запрещено

- ALL CAPS в хуках, self-reply, URL в теле, выдуманные цифры, advertising
- Pивот-история ($2M pre-seed) — отклонена Сергеем («ты как считаешь» → нет)

## Joint MoA (14.09)

- Рецензент 1: PASS-WITH-FIXES (anti-ad PASS; фикс: убрать «protection as an enabler» из собственной речи — применён)
- Рецензент 2: viral 64/100, scroll-stop обложки 8/10 («cover promises stop, text delivers how stops work»)

## Deadline

**Публикация:** approval получен 14.09 (Human Gate пройден). Токен: data/approval.token
