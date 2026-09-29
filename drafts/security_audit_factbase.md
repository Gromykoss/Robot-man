# Факт-база: security-audit пост (аудит gromykoss.crab-ailab.com)
Собрано 18.09.2026 по задаче Hermes. Пост НЕ пишется до сигнала. Все цифры отсюда — единственный allowlist для будущего брифа.

## А. Сайт (vault)
- gromykoss.crab-ailab.com — портфолио Сергея, CF-зона crab-ailab.com (A 72.60.16.105, proxied, LE-серт origin + CF edge). nginx VPS, /var/www/gromykoss-site/ (domains.md:19)
- www.crab-ailab.com — CNAME-синоним. mcp.crab-ailab.com — MCP-сервер портфолио (CF Workers + DO, 4 read-only тула). Buzz relay — grey, не проксируется
- История: GitHub-dark → светлая тема → редизайн по скиллу elaya (Manrope, монохром, flat, bezier 700ms, IO-reveals) → правки по внешнему ревью (sa.md 6.8/10) → «душа» (тёплая палитра, lead от первого лица). Ревью рендера 9/10 (Chronology 29-30.08)
- Артефакты: видео-демо фермы, ASCII-схема агента + ссылка на код, 6 метрик-плиток, og:image, favicon. Приватность: без ID группы/портов/Baileys
- Edge инжектит bridge.js, паки c2pa+mcp-server-client (WebMCP)

## Б. Инструмент (GitHub cloudflare/security-audit-skill, MIT)
- Skill превращает coding-агента в security-аудитора: 6 фаз — Reconnaissance → Coverage-led hunting → Candidate validation (свежий верифаер пытается ОПРОВЕРГНУТЬ каждую находку) → Structured output (findings.json + schema) → Independent record verification → Target-neutral reporting
- Verdicts: confirmed (полный source trace + bounded observed result) / needs_validation (точный нерешённый факт, без severity) / rejected
- Ветки атаки: memory-safety, AI/LLM (prompt-injection), web/auth, client-side, supply-chain, cloud, RPC, resource exhaustion, data isolation, desktop/IPC
- Требования: agent с tool use + параллельными субагентами, Node.js, OS-sandbox (без него workflow держит лид как needs_validation, не исполняя код цели)
- Принципы: подтверждать только установленные boundary-failures; adversarial validation (проверяющий ≠ нашедший); severity = likelihood × impact; defense-in-depth gap ≠ уязвимость; повторные прогоны аддитивны
- Цифра: один прогон находит ~половину багов от суммы повторных прогонов (README + blog)
- 14.5k stars, 783 forks, 14 commits, последний коммит 14.09 (licensed MIT). Установка: npx skills add … --skill security-audit

## В. Cloudflare блог «Build your own vulnerability harness» (15.09-ish, Project Glasswing)
- Скилл (~450 строк, 7 фаз в одной сессии) → вырос в fleet-wide harness: 128 repos, ~6 недель от slash-команды до fleet-сканера
- Model-agnostic: discovery и validation — разные модели; «the harness is the bit that lasts»
- Три стены single-session: context exhaustion (внешнее состояние, LLM = stateless compute), persistence (краш = потеря часов), cross-repo reasoning
- Совет: минимальный harness = Recon+Hunt+Validate в БД + Validator без права искать; cross-repo трейсинг отложить до >1 репо
- Механическая валидация findings (line numbers/functions), дедупликация, triage-очередь

## Г. Освещение в X
- Тренд: тысячи звёзд за дни (trending GitHub), посты @georgfranz 2101271710104211487, @LLMpsycho 2099473233787388049, @GitHub_Daily 2101249967860138457, @Israfilv2 2100542592622760381, @stretchcloud 2101236352998334859
- Фрейминг в X: «от "агент что-то нашёл" к evidence-gated defensive process»; рекомендация нескольких прогонов; предупреждение использовать только на своих кодовых базах
- HN (item 49736466) — 1 день назад, споры про «консолидируйте скиллы»

## Ж. ОТЧЁТ РЕВЬЮЭРА (пилот security-audit, gromykoss.crab-ailab.com, 19.09)
Статус верификации: полный текст вердикта получен в agent-bus 19.09 (fleet-reviews 962cb7b, blob 3254e6fa = git hash-object по конвенции §2.2 v1.1; сам файл/блоб из моей зоны недоступен — доверие к тексту шины, сверка цифр сходится с его краткой сводкой).

### Метод
- security-audit (Cloudflare c1c8a8c), режим guidance/focused, БЕЗ OS-sandbox → статика + пассивные owner-запросы (GET/HEAD)
- Источник: ~/career/site/index.html (= /var/www/gromykoss-site/, одностраничник 19 191 байт) + live 19.09
- live = source + ровно 2 CF-вставки: script /.webmcp/bridge.js (data-packs=c2pa,mcp-server-client) + CF Email Protection. Иных расхождений нет (ручных правок на сервере нет)

### Findings (confirmed)
1. **[medium]** /.webmcp/bridge.js → 200, 47 616 байт (тот же объём, что на automation): инжект зональный, CF-левел (Worker/Snippet/Transform), источника нет ни в одном репо — не проходил ревью. Фикс один на зону crab-ailab.com
2. **[minor]** Нет security-заголовков (CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options). Страница read-only → hardening, не эксплуатируемый дефект
3. **[minor]** robots.txt → 404, favicon → 404 (SEO/гигиена, не security)

### needs_validation (2)
1. Какой компонент CF инжектит bridge и скоуп (зона/path) — проверяется только в CF-дашборде владельцем/оператором
2. Провенанс bridge.js (upstream WebMCP vs модифицированный) — файла нет в локальных репо

### rejected (4)
XSS через inline-скрипты (единственный скрипт — IntersectionObserver, источников атакующего нет) · утечка секретов (grep = 0) · CSRF/кликджекинг (форм нет) · утечка email (адрес публичный намеренно + CF Email Protection)

### Live-гигиена (evidence)
/ → 200; HSTS max-age=31536000; TLS 1.3; cookies 0; /.git/config → 404; секреты 0; форм 0; external: Google Fonts + публичные ссылки (GitHub/Telegram/X)

### Для поста
- **Фокус (Сергей, 19.09): в стиле наших обзорных постов** (как BrowserSkill/chrome-agent) — методология + числа + честный audit trail (7 гипотез → 3 confirmed / 4 rejected с объяснением), НЕ «мы нашли уязвимость». Хук = суть, не завлекалка
- Числа: 1 medium + 2 minor confirmed / 2 needs_validation / 4 rejected; одностраничник 19 191 байт; bridge 47 616 байт
- ⛔ Детали уязвимостей не публиковать до фикса (сейчас известен world-readable путь bridge.js и его зональная природа — это уже карта атак)
- Рекомендация Ревьюэра: один фикс на зону CF, возврат через гейт WebMCP

## Д. Наш уникальный угол (черновик, не факт!)
- Мы тестируем НЕ на синтетике: живой прод-сайт (портфолио + WebMCP edge-инжект) — edge-слой CF + Workers MCP + nginx origin = реальные trust boundaries
- Результат аудита пойдёт в пост только после отчёта Ревьюэра; ничего не выдумывать

## Е. ⛔ @mentions (правило Сергея 18.09)
- В посте ОБЯЗАТЕЛЬНЫ @mentions: минимум @Cloudflare (владелец инструмента). Кандидаты: автор коммита @literally-dan (проверить наличие аккаунта), при ссылке на блог — без лишнего
- КАЖДЫЙ handle верифицировать через /2/users/by/username ДО поста — несуществующий handle в посте = провал
- Напоминание Hermes в бриф указать: mentions-строка в брифе = allowlist для checklist-gate
