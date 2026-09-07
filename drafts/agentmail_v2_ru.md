# AgentMail — RU draft v2 — 2026-09-03

**Правки Сергея:**  
1) без continuation-hook / без «хуков» в инженерных обзорах → кратко команда/стартап → продукт → опыт → выводы  
2) имена ящиков (gulag/gromykoss/robot-man@) — скрыть  
3) блок iCloud — убрать  
4) $6M / YC funding — убрать  

**Mentions (verified):** @agentmail · @haakamaujla  

---

## Факт-таблица (в пост)

| Факт | Ок |
|------|-----|
| @agentmail, CEO @haakamaujla | ✅ |
| General Catalyst backed (bio X) — без суммы/раунда | ⚠️ только если нужно; Сергей убрал $6M/YC — **не пишем funding** |
| inbox API, не AI-on-Gmail | ✅ |
| create inbox → real address @agentmail.to | ✅ |
| send/receive/threads/reply/attachments, MCP mcp.agentmail.to | ✅ |
| Hermes build guide на лендинге | ✅ |
| inbox-scoped key: auth.me scope=inbox; create → 403 missing_permission inbox_create | ✅ |
| org key: scope=organization → create OK | ✅ |
| free: 3 inboxes, 3000/mo, 100/day | ✅ |
| welcome inbound received; reply same thread_id; self-send = sent only | ✅ |
| messages.get без delivered/opened | ✅ |
| custom domain / footer / no calendar | ✅ |
| Gmail OAuth vs SendGrid send-only vs inbox-as-API | ✅ |

---

## RU-драфт v2

@agentmail строит email-инфраструктуру для агентов. CEO — @haakamaujla. На лендинге отдельно лежит guide под Hermes; MCP — mcp.agentmail.to. Позиция простая: не «AI читает твой Gmail», а inbox как API-объект, как Gmail для человека.

Продукт одной строкой: `inboxes.create` → живой адрес на @agentmail.to → send, receive, threads, reply, attachments. Free tier: 3 inbox’а, 3000 писем/месяц (send+receive в одном bucket), 100/день, 3 GB. Custom domain — с платного Developer. Calendar в продукте нет.

Зачем это агенту. Signup, OTP, magic link, support-thread — почти везде email. Без адреса агент ходит в сервис как инструмент без паспорта: browser может открыть форму, а verification уже чужой inbox или human OAuth.

Чем не заменяется. Gmail API заточен под human-аккаунт и OAuth. Transactional API (SendGrid/Resend и рядом) — в основном send-side: нет inbox/thread как first-class store. AgentMail держит address + persistent store + threading в одном API.

Свой прогон.

Первый ключ из console казался «широким». `auth.me` вернул `scope_type=inbox`. `inboxes.create` → 403, `missing_permission`, code `inbox_create`. В теле ошибки прямо: scope credential не покрывает create; organization-scoped key — самый широкий. Второй ключ с scope organization → `auth.me` = organization, create проходит. Урок: после Create API Key сразу `auth.me`, не доверять ощущению от UI.

Smoke на рабочем inbox: list/get; welcome inbound от admin@agentmail.to (`received`+`unread`); send; reply — тот же `thread_id`, что у welcome. Self-send на свой адрес остаётся `labels=[sent]`, как inbound loopback не появляется. В `messages.get` нет полей delivered/opened/bounced: «API принял отправку» ≠ «MUA показал во Входящих». Для delivery/bounce нужны webhook-события; для «письмо пришло мне» — list/WebSocket/webhook на `message.received`.

На free упёрлись в потолок 3 inbox’а: раздали разным агентам разные адреса и inbox-scoped ключи (least privilege). Org-key — только на create/admin, не в runtime агента.

Минусы, которые уже видны: shared @agentmail.to без своего домена; footer на исходящих на free; общая дневная квота send+receive; deliverability без прогрева своего домена; нет calendar в этом слое.

Вывод. Агенту для быта сети нужен не ещё один chat UI, а identity, который чужие системы уже умеют: email. Inbox-as-API закрывает create/send/receive/thread без human OAuth. Scope ключей (inbox vs organization) — первая грабля; `auth.me` дешевле, чем гадать по UI.

Building in public. 🤖

#BuildingInPublic #AIAgents #AgentMail #Email

---

## Открыто на ok
- Упомянуть General Catalyst из bio X? (без $ / YC) — сейчас **не** упомянул  
- Длина ок или ещё короче?
