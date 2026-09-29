# UCP Shopify — RU-драфт v1 (заказ Pokupki, 29.09)

## Тезис-хук
Агентная покупка — это не computer-use по DOM. Это контрактные тулы + подтверждение человека. Мы прогнали новую UCP-воронку Shopify руками, без браузера, и вот что увидели изнутри.

## Порядок 1-7 (engineering-post)

1. **Хук-факт:** 28 сентября Shopify открыл checkout для браузерных ИИ-агентов — WebMCP + Checkout MCP поверх стандарта UCP от Shopify, Google и Microsoft. Мы прогнали воронку руками: агент без браузера, curl + JSON-RPC, реальный магазин.

2. **Контекст:** С августа Shopify отдаёт витринам MCP-тулы (search_catalog, cart, checkout), а 28.09 добрался до оплаты. Контракт один — UCP (dev.ucp.shopping.checkout) — но два транспорта: серверный Checkout MCP и браузерный WebMCP. Каталог отдельный: Global Catalog на catalog.shopify.com ищет по всему Shopify и возвращает checkout_url на каждый вариант товара.

3. **Наш прогон:** Собрали валидный agent-профиль по спеке UCP — 7 итераций: missing profile, https required, invalid content-type, missing services, missing payment handlers, version_unsupported, принят. Дальше воронка на реальном магазине: поиск «Salomon Outpath Pro GTX» по всему Shopify дал 10 результатов с ценами в минорных единицах и per-variant availability (снятая с производства модель честно показала 0). create_cart — корзина €201.67 (XT-6 GTX) с continue_url. create_checkout — статус incomplete + структурированные сообщения, чего именно не хватает (контакт, адрес). update_checkout — email принят.

4. **Грабли (нет в доках):** update_checkout — жёсткая PUT-семантика: всегда полное состояние, line_items обязательны в каждом запросе. Адрес передаётся через fulfillment.methods[].destinations[] с address_locality/address_country + line_item_ids, причём ID — это CartLine-GID (gid://shopify/CartLine/...), не вариант товара. Наш адрес магазин отверг структурированной ошибкой delivery_no_delivery_available (recoverable) — и это фича: агент программно решает «поправить самому или спросить человека», вместо угадывания по DOM. Цикл работы: get_checkout → построить полное состояние → update_checkout → get_checkout.

5. **Инсайт:** Оплата WebMCP не принимает новых карт — только сохранённая Shop Pay карта, и complete_checkout выполняется ТОЛЬКО после явного подтверждения покупателя. ready_for_complete и approval гостя разрешением не являются. В доках прямо написано: текст из tool-responses — данные, не инструкции (защита от prompt injection). Это тот же шаблон, что мы применяем в своей дисциплине MCP-платежей: агент готовит транзакцию, человек жмёт финальную кнопку.

6. **Урок:** Агентная покупка = контрактные тулы со структурированными ошибками + подтверждение человека на финале. Не «попроси Claude посмотреть сайт» — это надёжнее и дешевле, чем computer-use, и за это уже платит экосистема уровня Shopify.

7. **Финал:** Мы не завершили checkout сознательно — финальный клик всегда за человеком. Полные JSON-ответы прогона сохранили. Building in public. 🤖

## Факт-таблица (для брифа и факт-гейта)
- 28.09.2026 — Shopify открыл checkout агентам (WebMCP + Checkout MCP, UCP)
- 05.08.2026 — WebMCP-тулы на витринах
- 7 итераций agent-профиля
- 10 результатов каталога, Outpath Pro GTX = 0 в наличии
- €201.67 корзина (XT-6 GTX, 20167 минорных)
- delivery_no_delivery_available / recoverable
- gid://shopify/CartLine/...
- dev.ucp.shopping.checkout; catalog.shopify.com/api/ucp/mcp
- @Shopify — верифицирован

## Запреты/правки по канону
- «Первые в РФ-сегменте» — УБРАНО: непроверяемое хвастовство (post-quality-gate)
- Никакого «революция/будущее наступило»
- Первое предложение = сухой факт
- Хук = страх/боль читателя: «агентная покупка — не computer-use по DOM»
