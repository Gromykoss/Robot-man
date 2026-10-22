# Fact-base: MCP-связь VPS-ПК (депозит Hermes, 21.10) — верифицировано robot-man 20.10/21.10

## Статус
Работает; владелец протестировал 21.10 ~09:30 UTC.

## Архитектура [CHRONOLOGY 21.10, Infrastructure Map]
- ПК: `ssh -N -R 127.0.0.1:18765:127.0.0.1:<MCP_PORT> mcptunnel@mcp2.crab-ailab.com` — обратный SSH-туннель
- VPS-приёмник: nginx 443 на mcp2.crab-ailab.com (Let's Encrypt certbot webroot, nginx-плагина нет) → 127.0.0.1:18765
- Bearer-токены ×2 (nginx map $http_authorization, без токена → 401)
- SSH-юзер mcptunnel: restrict,port-forwarding — только туннель, команд нет

## Верифицировано мной (live-пробы)
- `curl https://mcp2.crab-ailab.com/` без токена → **401** ✓ [мой curl 21.10]
- с неверным bearer → **401** ✓ (токен-гейт жив)
- endpoint живой и отвечающий

## Цифры [CHRONOLOGY 21.10, self-report Hermes + тест владельца]
- VPS-Hermes подключился к **hermes-pc 2.0.0**: initialize + session 4edbd5ef… + tools/list = **28 tools** (task_submit/result/approve, get/put_file, browser bsk_*, screenshot, conversations, permissions_respond)

## Проблемы, которые ловили (4)
1. Исходная схема CF named tunnel не взлетела (cloudflared на ПК не запускался) → погашена kill-switch: CNAME grok-bot.crab-ailab.com удалён (проверено: домен не резолвится), Access-приложение d7ebec2e удалено, туннель 4b9ee1b0 удалён cascade
2. Access Service Tokens нельзя создать API-токеном с Apps:Edit — только dash
3. nginx править ТОЛЬКО в живом sites-available — /tmp-копия откатила правку (регрессия Host поймана по 404 no community)
4. curl к 127.0.0.1:443 без --resolve ловит ghost-SNI 444

## Что НЕ проверено мной
- 28 tools / session ID — self-report Hermes + тест владельца; до драфта перепроверить live (initialize через bearer при ок)
- LE-сертификат (webroot) — не проверял

## Угол для поста
«VPS-агент управляет ПК-агентом через обратный SSH-туннель + MCP»: 28 тулов через bearer-гейт, kill-switch для мёртвой схемы, ghost-SNI-граб. Идеально в дугу «интернета агентов»: два агента на разных машинах, одна память.
