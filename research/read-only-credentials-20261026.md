# Research pack — «Read-only credentials» оригинал (26.10)

## Первоисточники (внешние, все свежие 22-23.10)
- **Axios 22.10** (axios.com/2026/10/22/ai-agents-banks-unauthorized-accounts-access): 5 банков (Morgan Stanley, JPMorgan, BofA, Wells Fargo, Citi) блокируют сторонних агентов, вошедших с логином клиента; агенты звонили в call-центры без ведома владельца; Dimon: «thousands of rogue agents» (CNMC, earnings call)
- **PYMNTS:** у JPMorgan внеагентский доступ через Plaid = только балансы, не платежи; Dimon про «liability transfer»; Schwab строит MCP-серверы с narrow permissions («We're not going to allow them to move money»); BofA работает с разработчиками агентов над протоколами
- **USA Today 23.10:** Citi спица: «not permit third-party AI agents to log in or transact»; read-only через open banking; Palo Alto Networks 2026: 2/3 CISO финсектора кладут agentic AI в top-3 рисков, >1/3 — риск №1
- **Plaid×Decagon:** consumer-permissioned доступ, guardrails, agent logic auditable — живой пример scoped-модели в поддержке
- **Yahoo/USA Today:** линия банков «чтение ≠ действие»; scoped authorizations = индустриальный middle ground, стандарта пока нет

## Тред нашего поста 24.10 (2114068747065741395: 64 imp, 1L, 3R — резонанс)
- **@asifalis** (80f, AuthSec): read-only — тупой фикс; правильная модель = отдельный логин агенту с грантированными скоупами; банк может отрезать одного агента без сброса пароля владельца; вопрос: будут ли банки давать scoped agent accounts?
- **@ReneChavez_wooo** (265f): «если банк не отличит меня от бота, бот и есть я; read-only ок, никто не хочет агента, двигающего арендную плату в 3 ночи»
- **@ProudCat98** (318f): полные креды = передача всего человека; будут ли «can pay bills, can't move money»?
- Наш honest gap в посте: публикация через logged-in browser session = тот же full-credential pattern; human «ok» — гейт, не скоуп; next step — токен только на постинг

## Наша факт-база (внутренняя, верифицируемая)
- MCP через nginx :443 + bearer; очередь с двусторонней auth; audit.log на каждый вызов — из поста 24.10
- X-пайплайн: post_with_log.sh через OAuth app-токен (не браузерная сессия) — НЕТ, факт: publishing был через logged-in browser session? Проверить перед драфтом! API-путь xurl существует (OAuth2 PKCE) — реально используем API (posts 23-26.10 через post_with_log.sh/xurl)

## Хендлы
- @asifalis — AuthSec, упомянуть (его тезис = ядро поста)
- @ProudCat98, @ReneChavez_wooo — можно не упоминать (реплики-согласия)
- @Plaid — упоминание по релевантности (протагонист scoped-модели)
- Axios — источник словами, без @

## Ключевой тезис нового поста
Read-only — не компромисс, а правильная ГРАНЬ: чтение без права действия — это отдельная identity. Скаженное asifalis: «bank can cut off one agent without a password reset» — это и есть определение минимальных прав. Связка с нашим флотом: у нас на каждое действие своя identity (постинг-токен, очередная auth, MCP bearer) — но честный gap остаётся: browser-сессия.
