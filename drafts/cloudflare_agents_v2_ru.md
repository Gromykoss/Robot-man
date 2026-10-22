# Cloudflare для агентов — RU-драфт v1 (02.10)

## Хук (страх читателя)
Половина трафика интернета уже не люди. Если твой сайт отвечает только людям, половина аудитории проходит мимо — и скоро за доступ к ней придётся платить тебе, а не наоборот.

## Факт-база (верифицировано первоисточниками)
1. **Ставка:** Radar — больше половины трафика сайтов на CF автоматический; модель «agentic internet»: readable, discoverable, callable, payable (Agents Week, авг)
2. **AI Search GA (01.10):** managed index + retrieval (Workers AI + Vectorize + R2 + Browser Run); нативный визуальный поиск (Qwen3-VL-Embedding, пиксели вместо капшенов; Matryoshka-эмбеддинги); OCR сканов PDF; файлы до 10 MiB (было 4); гибрид vector+keyword + rerank; биллинг с 01.11, free tier на всех Workers-планах — сам CF гоняет его на своём блоге и доках
3. **Monetization Gateway (closed beta):** «paywall для агентов» через HTTP 402 inline (без checkout-страницы); пер-request/per-token цены; расчёты через Coinbase x402 Facilitator, settlement в USDC на Base; 4 кейса в проде; для контента (прочитал один раз, использовали тысячу) — Pay Per Use: сеть верифицированных покупателей, отчитывающихся о каждом использовании
4. **Agents SDK v0.26 (01-02.10):** npm i agents; long-running агенты на Durable Objects — Pi (опенсорс harness) персистится между рестартами/крэшами/деплоями; «мозг» в DO, «руки» во внешнем sandbox (mattzcarey)
5. **Artifacts (open beta):** git-совместимая платформа для агентов — fork/clone/token/events на воркере; агенты уже «говорят на git»
6. **Инфраструктура бега:** песочницы Containers — старт быстрее ~6x, снапшоты ФС; Browser Run (ex-Browser Rendering) — Live View, human-in-the-loop, записи сессий; Kitesurf — браузер целиком на Workers, WebMCP
7. **Наблюдаемость (02.10, тема поста-триггера):** 8 апдейтов — logs, traces, analytics, alerts, dashboards, querying, telemetry export в одной платформе, предсказуемый прайсинг

## Кульминация
Стек сходится в одну картину: агент может **читать** (AI Search), **действовать** (Browser Run/Kitesurf/sandboxes), **думать с сохранением** (Agents SDK + DO), и **платить** (Monetization Gateway 402/USDC). Человеко-ориентированный веб получает параллельную экономику, где валюта — outcome, а не клик по рекламе.

## Урок/инсайт для наших
Мы в этом уже жили: WebMCP-чекaут Shopify — контракты вместо клика по DOM; UCP ready_for_complete ≠ разрешение; Web Bot Auth как идентичность. CF строит ровно ту же арку, но с платёжным рельсом.

## Не проверено
- Цены AI Search детально; «агенты >50% трафика» — заявление Radar (CF) — пометить в посте как их данные
- Бенчмарки Kitesurf vs конкуренты — только заявления
