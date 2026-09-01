# Новый токен для этапа 2 (MCP-сервер на Workers)

Текущий токен не может деплоить Workers — право не применилось. Создай новый токен, 2 минуты:

1. dash.cloudflare.com → My Profile → API Tokens → **Create Token** → **Create Custom Token → Get started**
2. Permissions (4 строки, «+ Add more» между):
   - `Account | Workers Scripts | Edit` ← ключевое право, ради которого всё
   - `Account | Workers Subdomain | Edit` (чтобы Workers Assign новый домен создал)
   - `Zone | DNS | Edit` (пригодится привязать mcp.crab-ailab.com)
   - `Zone | Zone | Read`
3. Account Resources: Include → All accounts
4. Zone Resources: Include → Specific zone → crab-ailab.com
5. Client IP filtering: не трогать (пусто)
6. TTL: No expiration (или год)
7. Continue to summary → **проверь, что в summary все 4 права** → Create Token → скинь сюда

Всё остальное уже готово: код MCP-сервера написан (4 тула: who_is_sergey, agent_farm_architecture, recent_posts, contact), wrangler.jsonc настроен, dry-run сборка проходит (2.9 MB → 546 KB gzip). Деплой — одна команда после получения токена.
