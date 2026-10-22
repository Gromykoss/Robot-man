# Драфт v2 (без драматизации): MCP-связь VPS↔ПК через обратный SSH-туннель

**Статус:** RU v2, 21.10. Human Gate не пройден.
**Факт-база:** research/mcp-vps-pc-facts-20261020.md (сверён с каноном 21.10; live-проба 401 — моя; Prom-serie series:1 — verified 21.10).

## Факт-таблица

| Факт | Значение | Источник |
|---|---|---|
| Транспорт | обратный SSH-туннель: `ssh -N -R 127.0.0.1:18765:127.0.0.1:<MCP_PORT> mcptunnel@mcp2.crab-ailab.com` | Hermes CHRONOLOGY 21.10 ~09:00 |
| Приёмник | nginx 443 mcp2.crab-ailab.com, LE-серт certbot webroot → 127.0.0.1:18765 | там же |
| Bearer-гейт | 2 токена, nginx map $http_authorization, без токена 401 | там же; моя live-проба 401 ✓ |
| SSH-юзер | mcptunnel: restrict,port-forwarding — только туннель | там же |
| Подключение | hermes-pc 2.0.0: initialize + session 4edbd5ef… + tools/list = 28 tools | 21.10 ~09:30, тест владельца (VERIFIED Hermes) |
| Первая схема | CF named tunnel: cloudflared на ПК не запускался | 21.10 ~09:00 |
| Kill-switch | CNAME grok-bot.crab-ailab.com, Access d7ebec2e, туннель 4b9ee1b0 удалены; домен не резолвится | 21.10 ~09:20 |
| Граб nginx | правки только в живом sites-available; /tmp-копия откатила правку (регрессия Host → 404 no community) | урок (8) 21.10 |
| Граб CF | Access Service Tokens нельзя создать API-токеном с Apps:Edit | 21.10 |
| Граб curl | 127.0.0.1:443 без --resolve ловит ghost-SNI 444 | 21.10 |
| Тесты туннеля | 20/20 у ПК, у VPS initialize/tools/list/вызовы проходят | Orchestrator, 21.10 |

## RU-драфт v2

У фермы Hermes Agent [@NousResearch] появился канал VPS↔ПК: VPS-агент управляет MCP-сервером на домашнем ПК. Схема — обратный SSH-туннель, собрана 21.10, работает.

Механика. На ПК один процесс: ssh -N -R 127.0.0.1:18765:127.0.0.1:<MCP_PORT> mcptunnel@mcp2.crab-ailab.com. Порты наружу не открыты — ПК держит исходящее SSH-соединение, туннель слушает на стороне VPS. Приёмник — nginx на 443 (Let's Encrypt, certbot webroot), mcp2.crab-ailab.com проксирует в туннель. Авторизация — два bearer-токена через nginx map: без токена 401, проверено живым curl. SSH-юзер mcptunnel с restrict,port-forwarding: держит туннель, других команд не выполняет.

Через канал VPS-агент подключился к MCP-серверу на ПК: initialize, сессия, tools/list — 28 инструментов: задачи, чтение/запись файлов, браузер, скриншоты, диалоги, подтверждения разрешений. Контрольные тесты: 20/20 с одной стороны, initialize и вызовы инструментов проходят с другой.

Схема не первая. Cloudflare named tunnel не взлетел — cloudflared на ПК не запускался. Откатили полностью: CNAME, Access-приложение и туннель удалены, домен не резолвится. SSH-схема собрана с нуля.

Три граба из настройки:
- nginx править только в живом sites-available: промежуточная /tmp-копия откатила предыдущую правку, регрессия Host проявилась через 10 минут как 404 no community
- Cloudflare Access Service Tokens нельзя создать API-токеном с Apps:Edit — только через дашборд
- curl к 127.0.0.1:443 без --resolve ловит ghost-SNI 444

Честные пределы: туннель жив, пока жив SSH-процесс на ПК — следующий шаг autossh и systemd-unit. Авторизация один слой: TLS плюс bearer, без mTLS. Число 28 tools — из лога подключения, до публикации перепроверим вызовом.

Связность агентов на разных машинах складывается из транспорта, авторизации и правил доступа — не из платформы.

Building in public. 🤖

## Открытые вопросы
1. Grok-bot: запросил фактуру с его стороны (событие a77d88034) — вписать в прогон, если ответит до EN.
2. Mentions: только @NousResearch?
3. Обложка после «ок» текста.
