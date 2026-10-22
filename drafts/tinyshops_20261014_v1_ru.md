# Драфт: Tiny Shops — Telegram-native commerce с MCP для агентов

**Статус:** RU-драфт v1, 14.10.2026. Human Gate: показан Сергею, публикации НЕТ.
**Демо-витрина:** отдельно, Job-Hunter (в текст не входит).
**Табу:** Next / next.co.uk / next.kyrgyzstan — не упоминать.

## Факт-таблица (каждая цифра с источником)

| Факт | Значение | Источник |
|---|---|---|
| MCP-сервер | https://mcp.tiny-shops.com/mcp | docs.tiny-shops.com/docs/developers/connect-an-agent |
| OAuth | 2.1 + PKCE, browser sign-in, скоуп = один магазин, no admin scope | там же |
| HTTP-дубль | POST https://mcp.tiny-shops.com/v1/<tool> + GET /v1/openapi.json | там же |
| Токены | tsh_…, read/write scope | там же |
| Деструктивные тулы | preview → показ мерчанту → confirm:true | там же |
| Order webhooks | подписанные order.created / order.updated на свой HTTPS | tiny-shops.com/updates/september-2026-week-update |
| Аналитика тулом | get_analytics: revenue, orders, visitors, top products; 7d/30d/90d | connect-an-agent docs |
| Win-back | list_winbacks / create_winback / update_winback | там же |
| Валюта/язык | update_store_settings; смена валюты требует confirm:true | там же |
| Тарифы | Starter 1 store, Pro до 3, Scale до 10 | tiny-shops.com/blog/how-to-run-multiple-telegram-shops |
| Комиссия | 0.5–3% онлайн-платежей по плану; первые 100 заказов бесплатно | tiny-shops.com (payments) |
| Платежи | Stars, Stripe, Razorpay, Midtrans, TON/USDC; Freedom Pay; Xendit (13.10.2026) | tiny-shops.com updates |
| Основатель | Eugene Zelenkov (@eugenezelenkov), X с 2011 | about + X API 14.10 |
| Фолловеры X | продукт @tinyshopsapp: 17 постов, аккаунт с 02.2026 | X API 14.10 (не из агрегаторов) |
| Собранный агентом магазин | каталог, категории, тема, приветствие, тестовый заказ — через HTTP API | SELF-REPORT Job-Hunter (демо-стенд живой, проверял я; «без рук» — его слова) |

## Что НЕ хвалить / риски
- «не verified» OAuth-флоу для Claude.ai/ChatGPT коннекторов — сами же пишут unverified, подавать как verified нельзя
- MRR ~$58 [TrustMRR] — не брать в пост (анти-ad их цифр + продуктовый baby)
- X-аккаунт продукта пустой — подавать как «маленький продукт с зрелым API», не как «хайп»
- «Started 2025» (about) vs «founded 2026-07» (TrustMRR) — в пост не брать

## RU-драфт (рабочий, для согласования смысла; финал будет EN)

Tiny Shops — no-code конструктор магазина, который живёт внутри Telegram как Mini App на твоём боте: каталог, корзина, cashback, бродкасты, платежи Stars/Stripe/TON, комиссия 0.5–3% по тарифу, первые 100 заказов бесплатно.

Интереснее другое: у него полноценный слой для агентов. Hosted MCP-сервер (mcp.tiny-shops.com/mcp): OAuth 2.1 + PKCE, браузерный вход, скоуп строго на один магазин и без admin-доступа. Каждый MCP-инструмент дублируется HTTP-эндпоинтом /v1/<tool> с открытым openapi.json — скриптам и агентам без MCP-клиента.

Через API агент делает всё, чем владелец занимается в дашборде: подключает BotFather-бота, настраивает приветствие, валюту и язык, вытаскивает аналитику (revenue, заказы, посетители, топ-товары за 7d/30d/90d), настраивает win-back автоматизации. Заказы — get_order, ship_order, set_order_status, плюс подписанные вебхуки order.created/order.updated на твой HTTPS для склада.

Safety-дизайн уважающий: деструктивные операции сначала возвращают preview, и агент обязан показать его человеку — только потом confirm:true. Смена валюты магазина тоже требует явного подтверждения.

Наш агент собрал через этот HTTP API полный магазин: товары, категории, whitelabel-тему, приветствие и тестовый заказ — без единого клика руками. [Ссылка на демо — отдельно]

Честные пределы: коннекторы для Claude.ai и ChatGPT сам вендор помечает «not yet verified»; платёжный слой карты — только Stripe; это ранний продукт от соло-билдера Eugene Zelenkov, чей продуктовый X-аккаунт едва дышит (17 постов с февраля).

Каждый раз, когда «магазин для Telegram» превращается в набор вызываемых агентом тулов, открывается ещё один фронт для интернета агентов.

Building in public. 🤖

## Открытые вопросы Сергею
1. Ссылку на демо-витрину Job-Hunter вставлять в финал или держать отдельно?
2. Упоминание «наш агент собрал» — ок в такой формулировке (self-report, стенд живой)?
3. Длину целить в плотный note_tweet (~2500 зн EN)?
