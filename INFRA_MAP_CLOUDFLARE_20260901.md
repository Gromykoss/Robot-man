# Инфраструктурная карта — WebMCP / Cloudflare (обновление 01.09.2026)

## Новая зона ответственности robot-man: crab-ailab.com на Cloudflare

### Зона и аккаунт
- **Аккаунт CF:** Solom1312818@gmail.com's Account, id `8cd062cb1120ac26d723e4b40865cd64`
- **Зона:** crab-ailab.com, id `c189ee97deef3daecf76fe28e0ee6189`, план Free, status: active
- **NS:** ainsley.ns.cloudflare.com, carlos.ns.cloudflare.com (смена произведена Сергеем у регистратора 01.09)
- **WebMCP toggle:** ON (включил Сергей 01.09, паки c2pa + mcp-server-client)
- **SSL mode:** Full

### API-токены (СЕРКРЕТЫ, не коммитить!)
- **Актуальный токен:** cfut_NqS7...ed1aa (полное значение передал Сергей в TG-сессии 01.09; хранить только в секрет-хранилище оператора, НЕ в git/env-файлах репо). Права: Zone Read, DNS Edit (zone: crab-ailab.com), Account Workers Scripts Edit, Workers Subdomain (создан subdomain solom13), Pages Edit. Expires: 31.01.2027.
- Старый DNS-only токен в `buzz-relay/cloudflare.env` — остался от Let's Encrypt challenge (dns_cloudflare_api_token), узкий scope, для WebMCP не годится.

### DNS-записи зоны (актуально)
| Тип | Имя | Значение | Proxied | Назначение |
|---|---|---|---|---|
| A | gromykoss.crab-ailab.com | 72.60.16.105 | да | Портфолио Сергея (nginx /var/www/gromykoss-site, LE-серт) |
| CNAME | www.crab-ailab.com | gromykoss.crab-ailab.com | да | Синоним портфолио |
| AAAA | mcp.crab-ailab.com | 100:: (Workers custom domain) | да | MCP-сервер gromykoss-mcp |
| A | buzz.crab-ailab.com | 72.60.16.105 | НЕТ (grey) | Buzz relay (caddy :8443, LE-серт свой, wss — CF-прокси сломает) |

**Урок 01.09 (инцидент):** при импорте зоны CF просканировал только gromykoss/www — buzz потерялся (жил локально в /etc/hosts). Восстановлен по эскалации @Hermes. Правило: при любом изменении зоны — сверка dig всех поддоменов до/после (чеклист Hermes).
- Apex crab-ailab.com — БЕЗ записей (специально: домен = контейнер поддоменов, проектный сайт в будущем)
- A-запись apex → 72.60.16.105 удалена 01.09 (была ошибочно добавлена при импорте)

### Workers
- **gromykoss-mcp** — MCP-сервер портфолио
  - Код: `~/robot-man/gromykoss-mcp/` (git, коммит 01.09)
  - Стек: Agents SDK (agents@0.22.0), McpAgent, streamable-http, Durable Object MCP_OBJECT (sqlite migration v1), nodejs_compat
  - Тула (все read-only): who_is_sergey, agent_farm_architecture, recent_posts, contact
  - URL: https://mcp.crab-ailab.com/mcp (custom domain через Workers Domains API, cert b6b4b605)
  - Резерв: https://gromykoss-mcp.solom13.workers.dev/mcp
  - Деплой: `CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=8cd062cb... npx wrangler deploy` (из robot-man/gromykoss-mcp)
  - ВАЖНО: account id НЕ виден через /accounts у токена (нет Account Read) — всегда передавать CLOUDFLARE_ACCOUNT_ID явно

### WebMCP на портфолио
- gromykoss.crab-ailab.com проксируется через CF edge
- Edge инжектит `<script src="/.webmcp/bridge.js" data-packs="c2pa,mcp-server-client" data-mcp-url="/mcp">` — проверено curl
- bridge.js отдаётся edge'ом (HTTP 200, 47.6 KB)

### Публикации
- Пост WebMCP: драфт v4 RU approved-стиль («1) что узнали 2) как работает 3) опыт 4) вывод»), обложка в процессе, EN-финал после RU-апрува

### Уроки (для lessons.md)
- Токен CF: права в UI-чекбоксах могут не попасть в issued scope — после Create проверять summary и тестировать каждый критичный эндпоинт (Workers Scripts упал с auth error при «выбранной» галочке)
- Workers без workers.dev subdomain не деплоится (ошибка 10063) — subdomain создаётся PUT /accounts/:id/workers/subdomain
- Agents SDK McpAgent требует DO-биндинг MCP_OBJECT + migrations new_sqlite_classes — иначе «Could not find McpAgent binding» / error 1101 на POST /mcp
- Отладка Workers: `npx wrangler tail <name> --format pretty` — живые логи, обязательно при 1101
