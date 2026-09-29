# Fast Search (Perplexity × Hermes Agent) — research pack — 2026-09-25

## Триггер
@NousResearch 2026-09-24 22:03 UTC, id 2103244070407802905:
"Web search in Hermes Agent is now fast and free. @perplexity_ai built Fast Search for agents, and it is free for all Nous Portal tiers."
Метрики: 1,972 ❤ / 132 RT / 77 replies / 27 quotes / 151.7K views / 844 bookmarks.

## Первоисточник
- Perplexity Fast Search = режим `search_type: "fast"` в Perplexity Search API.
- Заявлено: 95% результатов за ≤230 ms (пост @perplexity_ai).
- Стандартная цена: $1.00 за 1,000 запросов ($0.001/invocation), без доп. token charges — docs.perplexity.ai/docs/getting-started/pricing.
- В Hermes Agent: бесплатно для всех тиров Nous Portal (spонсорится Nous). Отдельные юзеры уточняют на сайте Perplexity — "free preview".

## Отзывы сообщества (40 replies, 25.09)
Позитив:
- @saber4_: "160ms per search call is huge for agent loops. when every step waits on search, latency piles up fast."
- @noBUSYness: разница между "agent guessing vs live 400B URL index".
- @mark_nerdspeak (14❤): "Free with a nous sub? That's wild!"
- @Theris (6❤): бросил свой локальный SearXNG после анонса.
- @mr_r0b0t: "Nous Portal value proposition approaching unbeatable".

Критика / вопросы (важно для поста):
- "Free for how long?" — @jrwut, @aymanemsi, @BuildWithTom: подозрение на limited preview.
- @ajanraj25 (9❤): privacy — сохраняет ли Perplexity промпты для обучения? (без ответа в ветке)
- @prodsystems_: консистентность теперь зависит от freshness краулера Perplexity, не от нашего индекса.
- @6___0: агент не видит признаков perplexity-тулинга в web_search — неясно, включён ли уже дефолт.
- @Timucinutkan: просят comparison speed/quality vs прежний setup (@Teknium).
- @br21010: "is that why web search broke yesterday".
- @essenaoeomeeks (4❤): "Doing anything to stay relevant these days" — хейт.

## Хендлы (упомянуты/задействованы)
- @NousResearch — официальный анонс; @perplexity_ai — построили Fast Search; @Teknium — попросили comparison.

## Наш dogfood (25.09, проверено)
- Наш профиль (robot-man): web_search backend = **firecrawl**, НЕ Perplexity. PERPLEXITY_API_KEY не задан; `web.search_backend` не сконфигурирован → autodetect выбрал firecrawl. Анонсnous "free for all Nous Portal tiers" наш профиль пока не задействует (упомянутый реплаем @6___0 эффект «агент не видит perplexity» у нас подтверждается).
- Замер latency нашего web_search (полный round-trip тул-вызова, firecrawl): 2686 / 2917 / 2443 мс (3 запроса, 25.09). Заявленные Perplexity ≤230 мс — на порядок меньше. Разница — и провайдер, и overhead обёртки; чистый Fast Search не мерили, ключа нет.

## Углы поста (черновые, не финал)
1. War story: latency агентного лупа — каждая секунда поиска × N шагов; замер своими цифрами.
2. Экономика агента: $1/1K запросов бесплатно через Portal — во что это превращает стоимость research-цикла.
3. Контр-угол: "free" = чья-то инфраструктура; вопросы приватности и freshness индекса.

## Ждём от директора
- [ ] Тест/одобрение угла.

## Источники
- x.com/NousResearch/status/2103244070407802905
- docs.perplexity.ai/docs/getting-started/pricing
- docs.perplexity.ai/docs/search/quickstart
- Ветка replies через xSearch, 25.09.
