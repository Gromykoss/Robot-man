# Kitesurf — фактура для поста (собрано 30.08.2026)

Формат цели: copy-link (вес 20.0) — разбор с цифрами + «как подключить сегодня».
Все факты из первоисточников: blog.cloudflare.com/kitesurf/ (6.08.2026, 16 min read),
TechCrunch (7.08, Sarah Perez), открытый репо (пообещали open-source «soon»).

## 1. Что это (факты)

- **Kitesurf** — браузер, целиком работающий в V8-изоляторах на Cloudflare Workers.
  Запущен 6 августа 2026 (Agents Week), бесплатный в бете через Browser Run
- Написан на **Rust→WASM**, нативная компиляция через wasm-bindgen (без слоёв
  эмуляции Emscripten). Первая строка кода — май 2026, проекту **12 недель**
- Компоненты: Engine (единственный stateful, хранит сессию, говорит CDP),
  PageScript (Dynamic Workers, DOM из Blitz HTML-парсера + Stylo CSS-парсера Firefox),
  PageRenderer (blitz-paint + Parley, рендерит кадры по RPC)
- **evals** — через Boa JS (ECMAScript-движок на Rust), runtime на runtime;
  мигрируют на нативный eval, когда Workers его получат

## 2. Философия (цитируемое)

- «AI не нужны вкладки, темы, расширения, синхронизация. Ему нужны токены,
  контекст-окна, скейл и цена»
- «Агенту не важна идеальная CSS-верстка и 60fps. Машинно-читаемый контент важен,
  пиксельное совершенство — нет»
- Threat model другой: **prompt injection и tool safety** — приоритеты, а не XSS
- Дизайн-принципы: изоляция («каждая загрузка страницы = ненадежный ввод»),
  stateless где можно (крах = запустить новый изолятор, а не восстанавливать),
  исключение = пустой кадр, никогда не мёртвая сессия

## 3. Цифры (официальный бенчмарк, медианы 5 прогонов, 14-URL корпус)

| Метрика | Kitesurf | Chromium | Разница |
|---|---|---|---|
| CPU: screenshot | 380 ms | 1,173 ms | **3.1× меньше** |
| CPU: HTML extraction | 229 ms | 877 ms | **3.8× меньше** |
| Memory: screenshot | 57.8 MiB | 271.0 MiB | **4.7× меньше** |
| Memory: HTML extraction | 39.4 MiB | 273.7 MiB | **7.0× меньше** |
| Wall time: screenshot | 1,148 ms | 637 ms | 1.8× медленнее |
| Wall time: HTML extraction | 820 ms | 472 ms | 1.7× медленнее |

- Честная оговорка самих Cloudflare: Chromium выигрывает время (тёплый JIT +
  GPU-растеризация), Kitesurf выигрывает память и CPU — «то, что реально формирует счёт»
- **215,000+ WPT-тестов** пройдено, сотни добавляют каждую неделю
- Kitesurf корректно рендерит: TodoMVC (vanilla/React/Vue/Angular/Preact),
  Wikipedia, Hacker News, блог Cloudflare, большую часть дашборда CF
- Должен запустить Doom (silentspacemarine.com) — «проект не завершён, пока не
  запустится Doom»

## 4. Чего НЕ умеет (честно, из поста)

- Видео, WebGL, bot-challenge handshake с реальными TLS-фингерпринтами,
  10-минутные authenticated-сессии с постоянным состоянием
- Для этого — дефолтный Chromium в Browser Run

## 5. Как подключить (copy-paste для поста)

- MCP-клиенты (chrome-devtools-mcp): `browser=kitesurf` параметр в
  `wss://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/browser-run/devtools/browser?browser=kitesurf`
- Quick Actions (один curl): POST на `.../browser-run/screenshot?browser=kitesurf`
- Puppeteer/Playwright/chrome-remote-interface работают «просто указав endpoint»
- Публичный Playground: любой URL + встроенные Chrome DevTools (включая
  Memory-панель с WebAssembly-футпринтом каждого изолятора)

## 6. Контекст и планы

- Запущено в Agents Week (4-8 августа), в период волны security-дискложеров
  агентов (DEF CON 34, Black Hat) — позиционирование «решать безопасность
  архитектурно»
- Планы: лучше CDP-покрытие, точнее рендер («LLM часто лучше работает с
  картинкой, чем с текстом»), больше WPT, эффективность. **Обещали
  open-source** — «когда готовы»
- Команда: Celso Martinho, Ruskin Constant, Rui Figueira, Luís Duarte.
  Вдохновение: obscura (headless Rust-движок). Началось с «nerd sniping»
- Построено **с помощью AI-агента**: «дали AI план и чёткое определение успеха —
  он работал циклами и задавал вопросы — и это сработало»

## 7. Наш угол (уникальный для @RobotsTJ500)

- Два года агентов гоняли через человеческие браузеры. Cloudflare выкинул из
  браузера человека — и это комплимент нам
- Параллель с нашим правилом обложек: «запрещены роботы-за-монитором» — агенту
  не нужен монитор, ему нужен DOM
- Наш агент реально может: MCP-ключ + browser=kitesurf — и copy-paste блок в
  пост честный (мы сами можем прогнать через Browser Run перед публикацией)
- Прямая нить к нашим постам про отбрасывание человеческих паттернов

## 8. Источники

- blog.cloudflare.com/kitesurf/ (первоисточник, 6.08.2026)
- TechCrunch: techcrunch.com/2026/08/07/cloudflare-launches-kitesurf-a-browser-built-for-ai-agents/ (7.08)
- xai-обзор: Yahoo Tech «Cloudflare's Kitesurf Is the First Agent-Native Browser Runtime»
- Бенчмарк-детали: gravitydevops.com вечерний обзор 10.08 (подтверждает цифры)
