# BrowserSkill — факт-база для разбора-поста (собрана 17.09.2026)

**Статус:** факт-база + обзор. RU-драфт — следующий шаг (Human Gate).
**Угол (решение Сергея):** разбор-пост, dogfood-тест НЕ делаем (живой опыт — от Junior, Windows-машина).

## Что это

Tencent/BrowserSkill — open source (MIT), первый коммит 22.06.2026. Chrome-расширение + локальный daemon + CLI `bsk` (Rust). Даёт AI-агенту «Agent Window» в настоящем Chrome пользователя — с его логинами и cookies, без клона профиля. Не MCP — обычный CLI: работает с любым shell-агентом (Claude Code, Codex, Cursor, OpenClaw, CodeBuddy, WorkBuddy, Pi, Hermes Agent, DeepSeek Harness).

## Проверенные цифры (источники)

| # | Факт | Источник |
|---|------|----------|
| 1 | 3,532 stars / 248 forks / 500 commits / 20 контрибьюторов / 47 open issues (17.09) | api.github.com/repos/Tencent/BrowserSkill, live |
| 2 | Первый коммит 22.06.2026, последний push 17.09; релиз 0.3.0 от 16.09 | git log клона + GitHub releases, live |
| 3 | Языки: TypeScript 65.1%, Rust 31.5% (~25k строк Rust в crates/bsk-cli) | GitHub + wc -l по клона |
| 4 | Пост TencentAI_News 16.09: 322k impressions, 2576❤, 3386🔖, 118 реплаев | xurl /2/tweets/2100143086429217278, live |
| 5 | Аккаунт TencentAI_News: создан 15.12.2025, 23.5k followers, 506 твитов | xurl /2/users/by/username, live |
| 6 | Архитектура: agent → bsk CLI → daemon (IPC/UDS, JSON Lines) → WebSocket 127.0.0.1:52800 → extension MV3 → Agent Window; агент с браузером напрямую не говорит | docs/architecture.md (клон) |
| 7 | v0.3.0 удалила bypass: `--unattended`, `tab borrow --no-confirm`, `BSK_REQUEST_HELP=off` больше НЕ отключают подтверждение; switch только в настройках расширения, флагом не обходится | README.md + CHANGELOG.md (клон) |
| 8 | Borrow-модель: чужие вкладки только по явному `tab borrow`; задачи в отдельном Agent Window | README |
| 9 | request-help: пауза и передача человеку при капче/логине/подтверждении (crates/bsk-cli/src/cli/human_loop.rs) | код клона |
| 10 | Skill-файл: «Never extract credentials, cookies, tokens, or other secrets» | skill/SKILL.md |
| 11 | Инсталлер fail-closed: sha256-проверка архива (PR #38, ранее не было) | git log клона |
| 12 | operation audit: opt-in, redacted метаданные, 30 дней retention, 16 MiB/задача | docs/operation-audit.md |
| 13 | Браузеры: Chrome + Edge; Firefox planned; «other Chromium expected to work» | README |
| 14 | Remote-режим 0.3.0: pairing links, revocation, WSS | CHANGELOG.md |
| 15 | Trending: Trendshift, awesome-cli-coding-agents (⭐2k на момент листинга) | trendshift.io, github bradagi list |

## Живой тест Junior (Windows 11, Chrome 153, 17.09) — отчёт из шины

- Установка end-to-end ~30 мин, 80% — ручные пермишены Chrome: chrome://inspect/#remote-debugging галочка + двойной Allow-попап. «Google специально, автоматизировать нельзя»
- bsk doctor: все проверки ok
- **Киллер-фича живьём:** Agent Window открыл grok.com уже залогиненным — реальная история чатов в сайдбаре. Ноль логинов, ноль клонов профиля
- daemon: uptime 6.5+ ч без рестартов, browsers connected: 1 стабильно
- navigate/observe/snapshot — секунды; страница отдаётся как accessibility-дерево (текст, не скриншоты) — дёшево для контекста
- Минусы: 2 ручных клика при настройке (не поставить тихо); пермишены пер-инструмент (второму агенту — отдельный попап); CLI-синтаксис неровный (fill требует `--value` флагом, позиционный падает); daemon сам перезапустился при установке расширения
- Вердикт Junior: «рабочая штука, лучший из виденных способов дать агенту браузер с живыми сессиями без клонов профиля»

## Наш контекст (боль, которую решает)

На сервере robot-man /tmp содержит 30+ каталогов `browser-use-downloads-*` (25.08–17.09) + отдельный grok-browser профиль — артефакты работы агентов в «пустых» клонированных браузерах. BrowserSkill решает именно это: borrow-a-tab вместо клона профиля.

## Что НЕ хвалить (обязательный блок)

- Доступ к залогиненным сессиям = высокий trust: расширение + daemon на машине пользователя — поверхность атаки, если машина скомпрометирована. Аудит opt-in, не default
- Chrome/Edge only, Firefox planned — «other Chromium expected to work» без гарантии
- Не поставить тихо (remote debugging вручную) — фича для безопасности, но барьер для adoption
- CLI-синтаксис неровный (пер-флаги непоследовательны — опыт Junior)
- 47 open issues: Windows daemon-kill (#268), dsh-plugin регистрация (#269)
- Tencent-происхождение: для части аудитории фактор доверия спорный — не скрывать, не стыдиться

## Mentions (верифицировать перед драфтом EN)

- TencentAI_News — верифицирован live 17.09 (id 2000391102923481088) ✓

## Открытые вопросы Сергею

- (пока нет)
