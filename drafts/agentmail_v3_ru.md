# AgentMail — RU draft v3 (развёрнутый) — 2026-09-03

**Правки Сергея (накопленные):**  
- инженерный обзор: **без хуков/continuation-серий**  
- порядок: команда/стартап → продукт → опыт → выводы  
- имена наших ящиков — **не светить**  
- iCloud-доставку — **не писать**  
- $6M / YC funding — **не писать**  

**Mentions (xurl verified):** @agentmail · @haakamaujla  
**Статус:** RU full. EN + cover после ok.

---

## Факт-таблица

| # | Факт | Источник |
|---|------|----------|
| 1 | @agentmail — Email Inboxes for AI Agents | xurl user + site |
| 2 | CEO @haakamaujla («Building things agents want @agentmail») | xurl |
| 3 | Продукт: inbox API, не AI-on-Gmail | docs introduction |
| 4 | Hierarchy: org → (pod) → inbox → thread → message (+ attachments) | docs inboxes |
| 5 | create → адрес @agentmail.to (custom domain с paid) | docs + pricing |
| 6 | send / receive / reply / threads / drafts / labels / attachments | docs |
| 7 | Realtime: WebSocket (без public URL) и webhooks (signed) | docs websockets/webhooks |
| 8 | MCP: https://mcp.agentmail.to/mcp | landing |
| 9 | Skills: npx skills add agentmail-to/agentmail-skills | landing |
| 10 | Hermes build page на сайте | agentmail.to/build/hermes |
| 11 | Free: 3 inboxes, 3000 emails/mo shared send+receive, 100/day, 3 GB | pricing + их blog free APIs |
| 12 | auth.me: scope_type organization \| pod \| inbox | API docs + наш вызов |
| 13 | Inbox-scoped key: create inbox → 403 missing_permission / inbox_create | наш smoke |
| 14 | Текст 403: scope не покрывает; organization-scoped widest | API body |
| 15 | Org key → create OK; затем inbox-scoped keys least privilege | наш прогон |
| 16 | Free потолок 3 inbox — заняли под разных агентов (имена не в пост) | API list count=3 |
| 17 | Welcome inbound: received+unread; reply → same thread_id | API |
| 18 | Self-send → labels [sent] only, не inbound mirror | API |
| 19 | messages.get: нет delivered/opened/bounced | API field list |
| 20 | Gmail API = human OAuth; transactional ≈ send-only; AgentMail = inbox object | docs + comparisons |
| 21 | Nylas = human connected accounts / agent accounts с calendar; мы calendar не тестировали | docs comparisons — осторожно |
| 22 | Transport исходящих у них через SES (message_id @email.amazonses.com) | наш send response |

---

## RU-драфт v3 (полный)

### Команда и стартап

@agentmail делает почтовую инфраструктуру под AI-агентов. Публичное лицо — @haakamaujla (CEO). В X-bio: email inboxes for AI agents. На сайте: SDK (Python/TypeScript), CLI, MCP, skills-пакет и страница setup под Hermes.

Их формулировка: *email for your AI*, не *AI for your email*. Не плагин над human Gmail — **inbox как first-class API resource**. Первый ops-check — не подпись кнопки Create API Key, а `auth.me`: organization vs inbox scope. Мы сожгли на этом цикл до любого полезного send.

### Продукт

**Модель данных.** Organization → опционально Pod (tenant isolation) → Inbox → Thread → Message (+ Attachment). Inbox — это «аккаунт» агента: свой адрес, свой store, свои треды. Не shared mailbox человека и не send-only endpoint.

**Базовый цикл.**
1. `inboxes.create` (org-scoped credential) → адрес вида `…@agentmail.to` (на free; custom domain — платный план).
2. `messages.send` / `messages.reply` — исходящие, threading через обычные email-заголовки.
3. Inbound: `messages.list` / `messages.get`, либо realtime WebSocket (`message_received` без ngrok), либо webhook на ваш URL (подписи — отдельный гайд).
4. Вспомогательное: drafts (human-in-the-loop), labels, lists (allow/block), attachments, search, metadata на inbox, inbox-scoped и pod-scoped API keys.

**Интеграции, которые важны runtime’у агента.**  
MCP endpoint `mcp.agentmail.to` — подключаешь в клиент с API key header. Skills: `npx skills add agentmail-to/agentmail-skills`. CLI: `agentmail-cli`. На лендинге явно размечен путь под Hermes (pip/npm + `AGENTMAIL_API_KEY`).

**Тариф free (проверено по pricing + их же free-API сравнению).**  
3 inbox’а · 3000 emails/месяц · 100/день · 3 GB. Квота **общая** на send и receive: одно исходящее + один ответ получателя = две единицы. Карта не нужна. Custom domain, снятие footer «Sent via AgentMail», EU/BYO cloud — не free.

**Чего в продукте нет (для наших задач важно).**  
Календаря как first-class identity (встречи/RSVP в том же grant) — это другой класс (например Nylas Agent Accounts). AgentMail = email identity + conversation store.

**Зачем агенту именно email.**  
Большая часть «быта» сети завязана на адрес: signup, OTP, magic link, support thread, transactional + reply. Browser-агент без inbox упирается в «Sign up to continue» и отдаёт verification человеку. С inbox verification и переписка остаются в API объектах thread/message — с `extracted_text` для ответа без quoted history.

**Чем не заменить из коробки.**
| Подход | Что даёт | Где ломается для агента |
|--------|----------|-------------------------|
| Gmail API / user OAuth | Deep read/send human mailbox | Human account, OAuth expiry, rate limits «как у человека», нет programmatic create inbox |
| Transactional (SendGrid, Resend, SES raw…) | Надёжный outbound | Inbound = webhook/raw MIME без inbox/thread store; нет «адреса агента» как сущности |
| Shared human inbox | Быстрый костыль | Нет изоляции агентов, audit смешан, ключи/сессии человека |
| AgentMail | Create inbox + two-way + threads + scoped keys | Свой домен/репутация — уже ops; free limits |

### Наш опыт (один прогон, без имён ящиков)

**Ключи и scope — главная грабля.**  
В console форма Create API Key предлагает Scope (entire organization / …) и Access (full within scope). Мы уже один раз унесли ключ, который *казался* широким. Проверка `GET auth/me` (SDK: `client.auth.me()`) вернула:

- `scope_type: inbox`
- `inbox_id` привязан к одному адресу
- `credential_kind: api_key`

С этим ключом `inboxes.create` → **403** `ForbiddenError`, `code: missing_permission`. В `message`/`fix` API прямо пишет: нет key-level restriction в том смысле, что create запрещён **scope’ом** credential; organization-scoped — widest; «создать ещё один key на том же scope не поможет».

Второй ключ с scope **Entire organization** → `auth.me` = `scope_type: organization`, `inbox_id: null`. Create проходит. После create для runtime агентов выпускали **inbox-scoped** keys (`inboxes.api_keys.create`) — least privilege: агент шлёт/читает только свой ящик, org-key не торчит в проде.

Практическое правило: **после любой Create Key — сразу `auth.me`**. UI-название и фактический scope могут разойтись в голове оператора; API не врёт.

**Smoke на рабочем inbox.**  
- `inboxes.list` / `get` — ок.  
- Inbound welcome от `admin@agentmail.to`: labels `received`, `unread`; body читается (`text` / `extracted_text`).  
- `messages.send` → ответ с `message_id` вида SES (`@email.amazonses.com`) и `thread_id`.  
- `messages.reply` на welcome → **тот же** `thread_id` (threading живой).  
- Self-send на свой адрес: в list остаётся `labels: [sent]`. Отдельного inbound-mirror «received самому себе» нет — для проверки receive нужен внешний отправитель или чужой MUA.  
- Поля `delivered` / `opened` / `bounced` в `messages.get` **отсутствуют**. Значит:  
  - «send вернул 200 + message_id» = провайдер **принял** отправку;  
  - «письмо у получателя во Входящих» без webhook `message.delivered` / `message.bounced` / human-сигнала **не доказуемо** из message object;  
  - «письмо пришло **мне**» = появление в list/WebSocket/webhook с `message.received`.

**Realtime vs poll.**  
Docs: WebSocket — persistent connection, subscribe по `inbox_ids` / `pod_ids`, события received/sent/delivered/bounced/…; public URL не нужен. Webhook — нужен ваш endpoint + verification. Poll `messages.list` — zero infra, платишь только вниманием и latency. Письма в квоту free входят; частый list сам по себе emails не сжигает.

**Лимит free на практике.**  
Три inbox’а — потолок. Мы упёрлись: один org, три агентных роли, три адреса, три inbox-scoped ключа. Четвёртый inbox = upgrade или удаление существующего. Org-key оставили только для admin/create; в runtime агентов — нет.

Если уже вшиваете почту в агентов: org-key только на provisioning и inbox-scoped в runtime — или один широкий ключ везде?

**Что сознательно не тащили в этот прогон.**  
Custom domain / DKIM своего домена, Agent Armor (beta request), production webhook endpoint, calendar-слой, x402 payment signup. Это следующие итерации, не сегодняшние факты.

### Выводы

1. **Email — всё ещё identity layer сети.** Пока signup/OTP/thread завязаны на адрес, агенту без inbox закрыта большая часть «бытовых» действий online.  
2. **Inbox-as-API** отличается от transactional send и от human Gmail OAuth: create address, store, thread, scoped keys.  
3. **Scope ключей — обязательный first check.** `auth.me` дешевле, чем отладка 403 на create. Org = provisioning; inbox-scoped = runtime.  
4. **Семантика статусов:** accepted send ≠ delivered to MUA; inbound себе = received event/list, не self-send label.  
5. **Free хватает** на multi-agent split (3 ящика) и engineering smoke; свой домен, footer, объём и репутация — уже product/ops решение.  
6. **В стек агента** (Hermes/MCP/skills) путь у них проложен; ценность не в демо «отправил письмо», а в том, что verification и переписка становятся tool-call’ами с thread memory.

Building in public. 🤖

#BuildingInPublic #AIAgents #AgentMail #Email

---

## Слабые места (Сергею)
- Сравнение с Nylas одной строкой — ок или вырезать (calendar не трогали)?  
- Таблица «чем не заменить» — оставить?  
- SES в message_id — деталь для инженеров или шум?
