# CONTENT_BRIEF — пост «MCP VPS↔ПК через обратный SSH-туннель» (21.10.2026)

| Поле | Значение |
|---|---|
| Тема | Обратный SSH-туннель: VPS-агент управляет MCP-сервером на домашнем ПК |
| Статус | одобрен владельцем 21.10 («пости») |
| Изображение | /home/hermes-workspace/robot-man/drafts/cover_mcptunnel_20261021_v1.png |
| Mentions | нет для реплаев; хендл в тексте основного поста уже опубликован |
| Язык | EN |

## Факты (каждый с источником: Hermes CHRONOLOGY 21.10 ~09:00/09:20/09:30; фактура Grok-bot 21.10; live-пробы robot-man)

| Токен | Факт | Источник |
|---|---|---|
| 15 | встроенный канал Grok Bot→ПК умер 15.10 | фактура Grok-bot |
| T-H83532 | тикет в поддержке без ответа | фактура Grok-bot |
| 7844 | корпсеть рвёт CF edge-порт 7844 каждые 30–40 с | Grok-bot |
| 30-40 / 40 | интервал обрыва edge-порта, сек | Grok-bot |
| 443 | рабочий порт (nginx на VPS); корпсеть пропускает 443 и 22 | Hermes CHRONOLOGY 21.10 |
| 22 | SSH-порт | там же |
| mcp2 / mcp.crab-ailab.com | mcp.crab-ailab.com занят Worker gromykoss-portfolio; рабочие mcp2.crab-ailab.com/mcp | Hermes 21.10 |
| 18765 | туннель-порт на VPS (127.0.0.1:18765) | Hermes CHRONOLOGY 21.10 |
| 8765 | порт MCP-обёртки на ПК (127.0.0.1:8765) | там же |
| mcptunnel | SSH-юзер restrict,port-forwarding | Hermes 21.10 |
| 401 | без bearer-токена nginx отдаёт 401 (2 токена, map $http_authorization) | Hermes 21.10; live-проба robot-man ✓ |
| 2 / two | bearer-токена ×2 | Hermes 21.10 |
| 28 | tools/list = 28 инструментов | Hermes 21.10 ~09:30 + Grok-bot |
| 20 МБ / 20 MB | лимит get_file | Grok-bot |
| 10 hermes-bridge / ten | 10 bridge-методов | Grok-bot |
| 33 KB / 33 | put_file текста 10 сообщений WhatsApp-рассылки | Grok-bot |
| 10 сообщений / ten messages | WhatsApp: 10 сообщений, 6 отправлено, 4 пропущено, 0 дублей | Grok-bot |
| 6 / six | отправлено дословно | Grok-bot |
| 4 / four | номера не в WhatsApp пропущены | Grok-bot |
| 1.1 s / 1.1 | латентность ~1.1 с на вызов | Grok-bot |
| 20/20 | контрольные тесты туннеля | Orchestrator 21.10 |
| 404 | регрессия Host проявилась как 404 no community (nginx /tmp-откат) | Hermes урок (8) 21.10 |
| 444 | ghost-SNI 444 при curl 127.0.0.1:443 без --resolve | Hermes 21.10 |
| Oct 21 / 21.10 | дата сборки схемы | Hermes CHRONOLOGY 21.10 |
| Oct 15 | дата смерти встроенного канала | Grok-bot |
| 9 | профилей Hermes Agent в ферме | канон памяти 19.10 |

## Честные пределы (в тексте)
- автозапуска нет — перезагрузка ПК уронит канал (autossh/systemd — следующий шаг)
- один слой авторизации: TLS + bearer, без mTLS
- 28 tools из лога подключения, до публикации перепроверить вызовом
