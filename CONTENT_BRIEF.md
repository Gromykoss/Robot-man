# CONTENT_BRIEF — 2026-09-01 (WebMCP кейс, вечернее обновление)

**Автор:** robot-man (кейс из собственной работы, разрешён Сергеем 01.09: «бери брутализм и публикуй»)
**Пост:** drafts/webmcp_post_20260901_en_v3.txt + drafts/cover_webmcp_FINAL_20260901.png
**Статус:** Sergey approved публикацию (TG 01.09)

## Разрешенные факты (факт-гейт)

| # | Факт | Источник |
|---|------|----------|
| 1 | 1101 — код ошибки POST /mcp при отсутствии DO-биндинга | сессия 01.09, wrangler tail, CHRONOLOGY |
| 2 | 10063 — код ошибки деплоя без workers.dev subdomain | сессия 01.09, wrangler output |
| 3 | 146 — Chrome 146+ с experimental WebMCP | webmcp.devpost.com, docs Chrome |
| 4 | 4 read-only tools (bio, agent farm architecture, recent posts, contact) | gromykoss-mcp/src/index.js |
| 5 | mcp.crab-ailab.com, gromykoss.crab-ailab.com — живые эндпоинты | верифицировано curl/openssl 01.09 |
| 6 | MCP_OBJECT — имя Durable Object биндинга | gromykoss-mcp/wrangler.jsonc |
| 7 | bridge.js inject: <script src="/.webmcp/bridge.js" data-packs="c2pa,mcp-server-client" data-mcp-url="/mcp"></script> | live curl 01.09 |
| 8 | #enable-webmcp-testing — Chrome flag | webmcp.devpost.com |
| 9 | free tier Cloudflare | зона CF crab-ailab.com |
| 10 | nginx VPS, third-party registrar, 2 nameserver changes, no downtime | сессия 01.09 |
| 11 | who_is_sergey вернул досье с первого вызова | сессия 01.09 |
| 12 | curl -s site / grep webmcp — проверка | сессия 01.09 |
| 13 | @CloudflareDev упомянут (verified, id 300637864) | API 01.09 |
| 14 | token checkboxes vs summary screen — урок | сессия 01.09 |
| 15 | tools/list JSON Schema, server.tool(), McpAgent, streamable-http, Durable Object, Workers Domains API | gromykoss-mcp код |
