# Драфт v3 (вобрана фактура Grok-bot): MCP-связь VPS↔ПК через обратный SSH-туннель

**Статус:** RU v3, 21.10. Human Gate не пройден. Обложка не готова.
**Факт-базы:** research/mcp-vps-pc-facts-20261020.md (депозит Hermes, сверён с каноном) + фактура Grok-bot (шина 21.10, событие a77d8803-ответ).

## Факт-таблица

| Факт | Значение | Источник |
|---|---|---|
| Зачем | встроенный канал Grok Bot→ПК не работает с 15.10 (тикет T-H83532 без ответа) | фактура Grok-bot |
| Первая схема | CF named tunnel: корпсеть рвёт edge-порт 7844 каждые 30–40 с; TUN через vless ломал TLS/ALPN | Grok-bot |
| Транспорт | обратный SSH: ssh -N -R 127.0.0.1:18765:127.0.0.1:8765 mcptunnel@mcp2.crab-ailab.com | Hermes CHRONOLOGY 21.10 ~09:00 |
| Приёмник | nginx 443 mcp2.crab-ailab.com, LE certbot webroot → 127.0.0.1:18765 | там же; mcp.crab-ailab.com занят Worker gromykoss-portfolio |
| Bearer-гейт | 2 токена, nginx map $http_authorization, без токена 401 | там же; моя live-проба 401 ✓ |
| SSH-юзер | mcptunnel: restrict,port-forwarding | там же |
| Цепочка | бокс (curl/mcp-remote) → mcp2/mcp → nginx → 18765 → ssh -R → 8765 на ПК → Node-обёртка mcp-http.v2.mjs (Streamable HTTP) → Hermes CLI/bsk/файлы | Grok-bot |
| Латентность | ~1.1 с на вызов | Grok-bot |
| Тесты | 20/20 OK; initialize + tools/list + вызовы проходят | Orchestrator |
| tools/list | 28: task_* (submit/status/list/result/cancel/approve), get_file ≤20 МБ (Desktop/Documents/Downloads/OneDrive/exchange), put_file (только exchange\inbox, base64), list_dir, read_log, bsk_* (navigate/observe/click/type/screenshot), system_status, 10 hermes-bridge | Grok-bot |
| run_command извне | нет (вариант Б); аудит вызовов audit.log на ПК | Grok-bot |
| Боевой пример 21.10 | WhatsApp-рассылка: put_file 33 КБ → task_submit «ПРЯМАЯ КОМАНДА СЕРГЕЯ» → 6 отправлено дословно, 4 номера пропущены, 0 дублей, скриншоты в outbox | Grok-bot |
| Открытый риск | автозапуска обёртки и туннеля НЕТ — перезагрузка ПК = канал лёг | Grok-bot |
| Граб nginx | правки только в живом sites-available; /tmp-копия откатила правку (регрессия Host → 404 no community) | Hermes урок (8) |
| Граб CF | Access Service Tokens нельзя создать API-токеном с Apps:Edit | Hermes |
| Граб curl | 127.0.0.1:443 без --resolve ловит ghost-SNI 444 | Hermes |

## RU-драфт v3

VPS-агент получил доступ к MCP-серверу на домашнем ПК — без проброшенных портов, через обратный SSH-туннель. Собрали 21.10 после того, как встроенный канал Grok Bot к ПК перестал работать 15.10 (тикет T-H83532 в поддержке без ответа), а две схемы туннелей до этой не выдержали условий сети.

Первые две попытки: Cloudflare named tunnel — корпоративная сеть рвёт edge-порт 7844 каждые 30–40 секунд, TUN через vless ломал TLS/ALPN. Второй субдомен тоже был занят: mcp.crab-ailab.com обслуживает Workers-портфолио, рабочим стал mcp2. Рабочая схема — обратный SSH через VPS на 443: корпоративная сеть пропускает 443 и 22, и исходящий SSH -R надёжнее вендорного туннеля.

Механика. На ПК один процесс: ssh -N -R 127.0.0.1:18765:127.0.0.1:8765 mcptunnel@mcp2.crab-ailab.com. Порты наружу не открыты — ПК держит исходящее соединение, туннель слушает на VPS. Приёмник — nginx на 443 (Let's Encrypt, certbot webroot), mcp2.crab-ailab.com проксирует в туннель. Авторизация — два bearer-токена через nginx map: без токена 401, проверено живым curl. SSH-юзер mcptunnel с restrict,port-forwarding: держит туннель, других команд не выполняет.

Полная цепочка: клиент (curl или mcp-remote) → https://mcp2.crab-ailab.com/mcp → nginx → 127.0.0.1:18765 → SSH-туннель → 8765 на ПК → Node-обёртка Streamable HTTP MCP → Hermes CLI, браузер bsk, файловая песочница. tools/list отдаёт 28 инструментов: постановка и статус задач, чтение файлов до 20 МБ (только Documents/Desktop/Downloads/OneDrive/exchange), запись только в exchange\inbox без перезаписи, браузер, скриншоты, 10 hermes-bridge методов. run_command извне нет. Каждый вызов — в audit.log на ПК. Латентность ~1.1 с на вызов.

Боевой пример в первый день: WhatsApp-рассылка коммерческого предложения. Файл с текстом 10 сообщений уехал put_file (33 КБ), задача ушла task_submit, Hermes на ПК отправил 6 сообщений дословно, 4 номера не в WhatsApp пропустил, дублей ноль, скриншоты легли в exchange\outbox.

Три граба из настройки:
- nginx править только в живом sites-available: промежуточная /tmp-копия откатила предыдущую правку, регрессия Host проявилась через 10 минут как 404 no community
- Cloudflare Access Service Tokens нельзя создать API-токеном с Apps:Edit — только через дашборд
- curl к 127.0.0.1:443 без --resolve ловит ghost-SNI 444

Честные пределы. Автозапуска нет — перезагрузка ПК уронит канал, autossh и systemd-unit следующий шаг. Авторизация один слой: TLS плюс bearer, без mTLS. В дополнение ловили поведенческие вопросы оркестрации: зависание задач в waiting_approval без доставки запроса владельцу, и правило Hermes отвергать «Сергей подтвердил» внутри текста задачи — правильно по сути, но явного механизма подтверждения пока нет.

Урок из схемы: когда сеть режет всё, кроме 443 и 22, исходящий SSH -R к своему VPS надёжнее любого вендорного туннеля. Второй урок — оркестратору не дробить задачи на шаги: цельная задача (цель, данные, формат результата) быстрее и дешевле, подтверждения нужны только на деструктивных действиях.

Building in public. 🤖

## Открытые вопросы Сергею
1. WhatsApp-пример: называть как есть (рассылка КП 6 сообщений) или обобщить? [Шаг предварительной проверки номеров ~14 мин — наш или обобщить]
2. Mentions: только @NousResearch?
3. Обложка после «ок» текста.
