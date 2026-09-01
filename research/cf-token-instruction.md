# Токен для robot-man (Cloudflare API)

Нужные права (Scoped, зона crab-ailab.com):
- Zone → Zone → Read
- Zone → DNS → Edit (создание/правка записей)
- Zone → Zone Settings → Edit (WebMCP toggle)
- Account → Cloudflare Pages → Edit (Pages-проект)
- Account → Workers Scripts → Edit (если пойдём в Workers для MCP-сервера)

Как создать:
1. dash.cloudflare.com → My Profile (иконка справа вверху) → API Tokens → Create Token
2. Custom token:
   - Name: robot-man-webmcp
   - Permissions:
     - Zone | Zone | Read
     - Zone | DNS | Edit
     - Zone | Zone Settings | Edit
     - Account | Cloudflare Pages | Edit
     - Account | Workers Scripts | Edit
   - Zone Resources: Include | Specific zone | crab-ailab.com
   - Account Resources: Include | твой аккаунт
3. Create → скопировать токен
4. Передать ЛЮБЫМ удобным способом (файлом сюда, или в чат) — я положу в секрет-хранилище, не в git
