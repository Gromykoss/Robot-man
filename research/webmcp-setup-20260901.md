# WebMCP — что нужно и как включить (для кейса @RobotsTJ500)

**Источник:** blog.cloudflare.com/webmcp/ (06.08.2026, Agents Week) + blog.cloudflare.com/agent-readiness/

## Что это

Переключатель в Cloudflare Dashboard (Agent Readiness > WebMCP) для любого домена в зоне Cloudflare:
- Edge инжектит в HTML одну строку `<script src="/.webmcp/bridge.js" data-packs="c2pa,mcp-server-client" data-mcp-url="/mcp">` — код сайта не трогается вообще
- Bridge в браузере посетителя регистрирует MCP-тулы через `document.modelContext.registerTool()` — браузерный стандарт WebMCP (экспериментальный в Chrome 146)
- Два пака в preview: **Content Credentials** (скан C2PA-метаданных изображений: `scan_images_c2pa`, `inspect_image_c2pa`) и **Site MCP Server** (прокси к своему MCP-серверу на том же домене `/mcp`)
- Всё выполняется в браузере посетителя, без раундтрипов на сервер Cloudflare
- Проверка за 5 секунд: `curl -s https://site.example | grep webmcp`
- Без своего агента — можно смотреть через BrowserRun (их remote browser)

## ЖЁСТКОЕ ТРЕБОВАНИЕ

**Домен должен быть зоной Cloudflare (proxied через их DNS/edge).** WebMCP инжектится на edge Cloudflare — если трафик не идёт через их прокси, инжектить нечего.

## Аудит наших доменов (проверено 01.09)

| Домен | Статус | Годится? |
|---|---|---|
| **spacegulag.online** | nginx @ Yandex Cloud (89.169.180.244), БЕЗ Cloudflare, webmcp нет | ❌ нет зоны CF |
| **crab-ailab.com** (apex) | DNS не резолвится (по lessons 30.08: apex без A/MX, поддомены живы) | ❌ apex мёртв |
| **buzz.crab-ailab.com** | поддомен жив (WSS-релей), локально в /etc/hosts указывает на 127.0.0.1; SSL-сертификат с hostname mismatch с внешней точки | ❌ не сайт, инфраструктурный поддомен |
| gromykoss.com | свободен | — |

**Итог: ни одного нашего домена сейчас за Cloudflare нет.** У SpaceGULAG — свой nginx на YC, у crab-ailab — живой только buzz-поддомен (релей, не сайт).

## Три пути получить проект на Cloudflare

### Вариант A — подключить spacegulag.online к Cloudflare (бесплатно)
1. Аккаунт Cloudflare → Add site → spacegulag.online (Free plan)
2. Сменить nameserver'ы у регистратора на выданные Cloudflare
3. Проксировать A-запись 89.169.180.244 (оранжевое облако)
4. Dashboard → Agent Readiness > WebMCP → toggle ON → выбрать паки
5. Проверка: `curl -s https://spacegulag.online | grep webmcp`
- Плюсы: реальный сайт с аудиторией, GULAG-проект (сюжет). Минусы: трогаем прод GULAG-отдела — нужно согласование с Alikhan... нет, GULAG — свой отдел, согласование с GULAG-агентом + Сергеем. SSL в режиме Full.

### Вариант B — мини-сайт на Cloudflare Pages (новый проект)
1. Deploy статического сайта (агентские портфолио/статусы) на Pages — бесплатно
2. Домен *.pages.dev уже за Cloudflare, или привязать свободный домен
3. WebMCP toggle → контент готов
- Плюсы: ничего не трогаем в проде, чистый демо-кейс. Минусы: нужен смысловой сайт (что на нём лежит? статусы агентов? портфолио команды?)

### Вариант C — MCP-сервер вместо пассивного сайта
Site MCP Server pack проксирует к своему `/mcp` — можно поднять свой MCP-сервер с тулами (статус стройки, ЕЖО-сводка, search по CHRONOLOGY). Тогда агенты посетителей могут ЗАПРАШИВАТЬ данные. Это уровень 2 кейса.

## Рекомендация
**Вариант B** (Pages + свободный домен или pages.dev): ничего не ломаем, полный контроль, кейс чистый. Затем Вариант C (свой MCP-сервер с тулами статусов) — это уже вторая часть истории и сильный контент. Вариант A — опционально позже, с согласования GULAG-отдела.

## Что спрашиваю у тебя:
1. Какой вариант? (рекомендую B→C)
2. Если B: есть свободный домен под это, или пусть будет `<что-то>.pages.dev`?
3. Если поднимать свой MCP-сервер — какие тула открывать наружу? (моё предложение: read-only статусы + search)
