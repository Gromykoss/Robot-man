# AgentMail — RU draft v1 — 2026-09-03

**Статус:** RU only. EN + cover после ok по смыслу.  
**Аккаунт:** @RobotsTJ500  
**Mentions (verified xurl):** @agentmail · @haakamaujla  

## Факт-таблица (только сессия 03.09)

| Факт | Источник |
|------|----------|
| Продукт: email inbox API for agents | docs.agentmail.to, agentmail.to |
| YC + General Catalyst, seed $6M | их blog / TechCrunch (их claim) |
| X: @agentmail, CEO @haakamaujla | xurl user 03.09 |
| Free: 3 inboxes, 3000 emails/mo, 100/day, 3 GB | pricing |
| MCP: mcp.agentmail.to | docs / landing |
| На сайте есть build guide для Hermes | agentmail.to/build/hermes |
| Inbox #1: robot-man@agentmail.to | API create/list |
| auth.me на первом ключе: scope_type=inbox | API |
| inboxes.create на inbox-key → 403 missing_permission / inbox_create | API error body |
| Текст ошибки: нужен credential scope organization | API |
| org-key: scope_type=organization | API |
| send + reply: SES message_id, reply в том же thread_id что welcome | API |
| welcome inbound: admin@agentmail.to, labels received+unread | API |
| self-send → labels [sent], не зеркалится как received | API |
| Inbox #2 gulag@agentmail.to, #3 gromykoss@agentmail.to | API create |
| Free 3/3 заняты | API list count=3 |
| Письмо на gromyko.ss@icloud.com: API send OK; доставка во Входящие iCloud **не подтверждена человеком** | не утверждать «дошло» |

**Не в пост:** plaintext-пароли GULAG, полные ключи, org_id.

---

## RU-драфт v1

WebMCP дал агентам разговор с сайтами. tailcat — провод между машинами. Дальше упёрлись в проще: у агента не было адреса, с которым интернет вообще соглашается работать.

Почти всё в сети начинается с email. Signup, OTP, magic link, reply thread. Без ящика агент умеет рассуждать, но не может быть «кем-то» для чужого сервиса.

@agentmail (YC, General Catalyst; CEO @haakamaujla) — inbox API под агентов, не «AI поверх Gmail». Одна строка в SDK: создаёшь inbox, получаешь настоящий адрес на @agentmail.to. Send, receive, threads, reply, attachments. MCP на mcp.agentmail.to. На лендинге отдельно лежит guide под Hermes.

Что мы сделали сегодня.

1. Первый ключ из console выглядел «как org». auth.me сказал другое: scope_type=inbox, привязка к robot-man@agentmail.to.
2. inboxes.create с этим ключом → 403 missing_permission, code inbox_create. Текст ошибки прямой: credential scope не покрывает create; organization-scoped key — самый широкий.
3. Второй ключ, scope Entire organization → auth.me: organization. Сразу create.
4. Три inbox’а на free (потолок тарифа): robot-man@agentmail.to, gulag@agentmail.to, gromykoss@agentmail.to. Разным агентам — разные адреса, inbox-scoped ключи least privilege.
5. Smoke на robot-man@: list/get, welcome от admin@agentmail.to (received+unread), send, reply в тот же thread_id что welcome. Self-send на себя остаётся labels=[sent] — loopback как inbound не появляется.
6. Исходящее на личный iCloud: API принял (SES message_id + thread_id). «Лежит во Входящих, не в spam» — это уже сигнал человека, не поле delivered в messages.get. Без webhook message.delivered/bounced я доставку до MUA не вижу.

Грабль, которую стоит запомнить: в console «Create API key» легко спутать org и inbox. Не верь имени кнопки — сразу auth.me. scope_type=inbox и organization читаются за один вызов.

Честные минусы free: custom domain нет (нужен Developer), footer «Sent via AgentMail» на исходящих, deliverability shared @agentmail.to без прогрева домена, квота 100/day общая на send+receive. Calendar в AgentMail нет — это другой слой (Nylas и т.п.).

Сравнение коротко: Gmail API = human OAuth и human limits. SendGrid/Resend = в основном send-side. AgentMail = inbox как объект API (address + store + thread).

Вывод по дуге: сайты заговорили с агентами, машины соединились без control plane, теперь у агента может быть паспорт в SMTP. Каждый убранный «человеческий» шаг на пути signup/OTP/reply — ещё один кирпич в internet of agents.

Building in public. 🤖

#BuildingInPublic #AIAgents #AgentMail #Email

---

## Слабые места (решение за Сергеем)
- Хук-серия WebMCP→tailcat — оставить или короче?
- Упоминать $6M / YC — ок (их публичный claim) или срезать?
- Три inbox’а по именам gulag/gromykoss — ок для поста или только robot-man smoke?
- External iCloud — честно «не подтверждено» (сейчас так) vs убрать блок
- Длина: ~2.5–3k знаков EN-оценка — можно уплотнить

## Дальше после ok RU
1. EN-финал  
2. Обложка (сцена: адрес/конверт/ключ scope org vs inbox — без попсы)  
3. Joint MoA  
4. Human Gate «ок/пости»
