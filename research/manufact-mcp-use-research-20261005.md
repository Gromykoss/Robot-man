# Research Pack — Manufact (ex mcp-use) — кандидат для инженерного поста

Составлено 2026-10-05 (этап 2, радар-протокол: исследование СНАРУЖИ, без регистрации).
Сергей выбрал кандидата №3 из радара (Synaptic Tip-Offs #51).

## 1. Первоисточник

- **Сайт:** https://manufact.com/ (ex mcp-use). GitHub SDK: https://github.com/mcp-use/mcp-use (~10.7k звёзд).
- **YC launch:** https://www.ycombinator.com/launches/O2c-mcp-use-open-source-infrastructure-and-dev-tools-for-mcp-agents —YC S25.
- **Docs SDK:** https://docs.mcp-use.com/ (TS + Python quickstart; `npx create-mcp-use-app@latest`).
- **Docs Cloud:** https://docs.manufact.com/
- **X:** https://x.com/manufact (официальный).
- **Фандинг:** $6.3M Seed (февраль 2026), YC S25. Founder: **Pietro Zullo** (YC launch автор).
- **Claim-цифры (их, не наши):** 7M+ downloads Python+TS, ~10k звёзд; используют «20% US500», NVIDIA, IBM, Intuit, Red Hat, Tavily — все цитаты только из их материалов.

## 2. Что это (суть)

«MCP cloud»: open-source SDK (mcp-use) + managed cloud (Manufact) для сборки/деплоя/обсервабельности MCP-серверов и MCP Apps. Один кодбейс — везде: ChatGPT Apps Store, Claude Connectors, Gemini, Cursor, Claude Code. Их метафора: «mcp-use SDK — это Next.js для MCP SDK».

Ключевые модули облака: Hosting, Cross-client testing (одни проверки на ChatGPT+Claude), Publishing checks (аудит под требования Apps Store), Submission Pack, Cloud Inspector (trace/replay MCP-трафика), Public chat, Analytics (latency/reliability).

SDK: MCP Server/App/Client/Agent + интерактивные Views (React) внутри ChatGPT/Claude — tool с view, end-to-end типизация (zod).

## 3. Экономика (pricing 05.10.2026, их страница)

- **Free:** $0, $5 кредитов/мес, 2 проекта, 30k requests/мес, publishing checklist, community support. **Нам достаточно для dogfood.**
- Hobby $25/мес ($300/год): 5 проектов, 300k req, evals, e2e-checks.
- Startup $250/мес; Enterprise от $1000/мес.
- Credits reset ежемесячно; pay-as-you-go сверху; spend limit настраивается.

## 4. Как участвовать (путь для нашего агента)

1. Free-аккаунт → connect GitHub repo → deploy MCP-сервера.
2. Локальный путь без облака: `npx create-mcp-use-app@latest` → `mcp-use dev/build/start`; Python quickstart тоже есть.
3. Tunneling: локальный MCP-сервер наружу через secure tunnel (без облака).
4. mcp-use Inspector: дебаг MCP-серверов из браузера.
5. client CLI: подключение к MCP-серверам из терминала.

## 5. Кандидатная тема поста (для брифа)

Наш dogfood-угол: мы уже живём в MCP (самодельный X MCP bridge). Кейс: «собрали мини-MCP-сервер на mcp-use SDK (TS) — сколько минут до рабочего тул-колла; что дают Views внутри ChatGPT; Cloud Inspector против самодельных логов». Плюс макро-угол: MCP как слой дистрибуции продукта (real estate внутри ChatGPT/Claude, 800M+ пользователей — их claim).

## 6. Риски

- ⚠️ **npm/npx стороннего пакета** (`create-mcp-use-app`) — проверять пакет до установки (`npm view mcp-use`, авторы, downloads, версия с пиннингом) — протокол skill.
- Cloud Inspector/Analytics — облако: данные тул-коллов уходят на их хостинг; для поста показывать на демо-сервере, не на нашем проде с ключами.
- Managed-зависимость: бесплатный тариф ok, ничего не платим; не привязывать прод-пайплайн.
- TS-first: наш стек питон — питон-ветка SDK есть, но слабее TS; проверить в этап 3.
- Стартап 2-летней стадии с облаком — упоминание через mention-gate skill при драфте.

## 7. Ждём от директора

- [ ] Апрув этапа 3: регистрация free-аккаунта (email — спросить owner_email Сергея).
- [ ] Апрув на установку npm-пакета mcp-use на сервер (пиннинг версии).

## 8. Источники

manufact.com/, pricing, YC launch, docs.mcp-use.com (llms.txt), synaptic Tip-Offs #51, x.com/manufact. Все цифры выше — из первоисточников, дата фиксации 2026-10-05.

## 9. Dogfood прогона 05.10 (этап 3, локальный путь)

- npm: `mcp-use@2.7.3` (пиннинг), 51 пакет; npm-гвард: версии 1.4.2/1.4.3 помечены malicious (OSSF) — **2.7.3 не затронута**, пиннинг обязателен. Downloads last week: 41,469 (api.npmjs.org 05.10).
- node v26.8.1, tsx v4.23.15.
- Собран демо-сервер `dogfood/mcp-use-probe/server.ts` (MCPServer + 2 тулов: recent_posts из published_posts.jsonl, graph_stats из graph.json).
- Прогон: HTTP MCP на localhost:3000 (initialize → 200, protocolVersion 2025-06-18); клиент probe.ts: TOOLS: recent_posts, graph_stats; recent_posts OK; **graph_stats: {"entities":494,"edges":475}**.
- Нюансы SDK (для поста): top-level await требует `"type":"module"`; output schema требует return с structuredContent (иначе validation error); stdio-режим не автозапускается — нужен `server.listen(3000)` (HTTP) или `mcp-use dev/start`; TS-first (typecheck via mcp-use CLI).
- ⛔ Блокер регистрации free-аккаунта: браузер-сессия Hermes на сервере падает ("Session name 'default' is too long. Socket path 112B > max 103B") — доложено Hermes в agent-bus. Регистрация/Cloud Inspector — после починки.
