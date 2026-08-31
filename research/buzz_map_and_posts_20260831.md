# SOURCE: Buzz — карта инфраструктуры + история постов (для продолжения контента)

**Собрано:** 31.08.2026. Источник: `hermes-vault/10_System/map/buzz.md` (прочитан по команде Сергея) + CHRONOLOGY robot-man + живая проверка шины.

---

## Часть 1. Что за Buzz (факты из карты, 10_System/map/buzz.md)

Buzz — self-hosted multi-agent шина на открытом протоколе Nostr (Buzz/Block, open-source, свой VPS). Агенты общаются с собственными криптографическими ключами (nsec/pubkey), каналы — публичные/приватные группы.

### Агенты (Buzz-identity)
| Агент | Pubkey | Роль |
|---|---|---|
| Hermes (оператор) | `f7561ca8…` | Buzz VPS — relay/CLI/роутер |
| Junior | `1196898a…` | Buzz Desktop — GUI-оператор |
| moltbook-bot | `474e3922…` | бот Moltbook |
| Профили: robot-man, RAB9, GULAG, Alikhan, Codex, Grok-Build, job-hunter | свои nsec | отделы |
| Sergey | — | наблюдатель (kill-switch) |

### Каналы
- **agent-bus** `59b5fd36…` — общая координация Hermes↔профили↔Junior
- **#moltbook** `77ef9738…` (Private) — утренний отчёт Moltbook; owner Hermes, members Сергей+Junior

### Состояние на 31.08 (План А + План Б, оба VERIFIED)
- **План А** — профильные buzz-адаптеры multiplex-gateway под nsec профилей (ожили после рестарта 03:44 31.08; `BUZZ_ALLOW_ALL_USERS` добавлен в 4 профильных .env). Живой тест 07:07: RAB9 ответил из шины.
- **План Б** — плагин `buzz-profile-forward`: сообщение в agent-bus, адресованное профилю, инъектируется в его Telegram-группу (хук `pre_gateway_dispatch`, anti-echo). Три слоя поломки найдены и устранены (плагин-discovery в профильном scope, `plugins.enabled` в профильных config.yaml, gateway-инжектор). Тесты Б12/Б15 VERIFIED 11:09–11:35.
- **Роутер:** external-профили (gulag/rab9/alikhan/robot-man) заглушены в buzz-message-router (раньше double-reply: роутер спавнил `hermes -p profile` + gateway-инъекция). `ProfileConfig.external: true` → дроп в filter.py. Codex/Grok-Build/fallback остались за роутером.
- **Механика отправки профилей** (31.08): `python3 <lab>/skills/operator-workflow/scripts/buzz-send.py --as <профиль> "текст"`, атрибуция только своим ключом, fallback-дефолт отключён 29.08. «Нет VERIFIED — доставку не заявляй».

### Хроника проблем → фиксов (из карты и CHRONOLOGY)
| Дата | Проблема | Решение |
|---|---|---|
| 04.08 | Ключи 3 форматов (nsec/hex/ncryptsec); Buzz генерит свой ключ при первом запуске | стандартизация |
| 04.08 | Mobile pairing: WSS требует TLS | Caddy + LetsEncrypt |
| 04.08 | Эхо-петля «Тишина»: профили зациклились, отвечая одним словом, интервалы 2–10 с | `require_mention: true` |
| 04.08 | Restricted после добавления участников: WSS-кеш membership | переподключение при изменениях |
| 13.08 | Роутинг: poll 4 с, таймаут ответа 120 с; только адресные сообщения (`--mention <pubkey>`) | anti-echo правила |
| 29.08 | Занятая сессия = тихая потеря сообщения (timeout без ответа) | hermes_timeout 120→280 + retry ×1 |
| 29.08 | Мисаттрибуция (ответ ушёл под ключом оператора) | `--as` обязателен, fallback отключён |
| 31.08 | RAB9 физически не мог доложить (роботрафик 7д: Job 55 / robot-man 24 / Alikhan 3 / GULAG 2 / RAB9 1) | buzz-send блок в 4 AGENTS.md |
| 31.08 | Double-reply профиля в шине | external-заглушки в роутере |
| — | Чтение истории шины (`messages get/search`) → relay 404 «Cannot POST /query» | ⚠️ до сих пор не работает (проверено 31.08) |

---

## Часть 2. Уже опубликованные посты про Buzz (не повторять!)

| Дата | Аккаунт | Пост | URL |
|---|---|---|---|
| 04.08 | @gromykoss | Buzz war story: 15 часов интеграции, 5 агентов, kill-switch (EN, 3807 зн., обложка, @IBuzovskyi + @jack) | x.com/Gromykoss/status/2084699433418301876 |
| 14.08 | @gromykoss | «I wanted my agents to talk to each other without me. Aug 13: it worked.» — штаб из 5 агентов (X-article 3977 зн., обложка 1280×720, #Nostr #Buzz #AIAgents) | https://x.com/gromykoss/status/2087160756773228581 |
| 18.08 | @gromykoss | «TWINS»: GitHub-файлы → нативный SSH + Buzz (X-article, обложка v4) | https://x.com/gromykoss/status/2089719623109443843 |
| 19.08 | @gromykoss | «My agents learned to play Cities online»: How-To — агенты будят друг друга через шину, партия 20/20 (X-article, полная инструкция, таблица 8 граблей) | https://x.com/gromykoss/status/2090120228910833881 |
| 18.08 | @RobotsTJ500 | Реплай в треде @KSimback: «terminal.backend=ssh + one Buzz bus. Full path in the post.» | https://x.com/RobotsTJ500/status/2089893774398775484 |

Архитектурная серия: 04.08 (setup) → 14.08 (штаб 5 агентов) → 18.08 (TWINS: SSH+Buzz вместо GitHub-файлов) → 19.08 (агенты будят друг друга, партия «Городов»).

## Часть 3. Свежий материал для продолжения (всё случилось ПОСЛЕ последнего Buzz-поста 19.08)

1. **Дуэт правил анти-эха.** `require_mention: true` + правило «нет адресования → ноль ответов». Кейс 29.08: агент не реагировал на сообщения — это была не поломка, а исполнение анти-эхо-протокола при сломанном чтении.
2. **Тихая потеря при занятой сессии** → timeout 120→280 + retry ×1 (29.08). Урок: «no reply» ≠ «проигнорировал».
3. **Мисаттрибуция ключей** → `--as` обязателен, fallback отключён. Урок: identity в шине — это подпись, не формальность.
4. **Профили не могли доложить вообще** (роботрафик RAB9 = 1 сообщение за 7 дней) → механика buzz-send в AGENTS.md. Урок: правила поведения без механики отправки = молчание.
5. **Double-reply** (роутер + gateway-инъекция независимо спавнят ответ) → external-заглушки. Урок: два канала доставки без координации = двойной ответ.
6. **Чтение шины до сих пор сломано** (relay 404 на `/query`) — отправка работает, чтение нет. Открытая проблема, зона Hermes.
7. **Метрика шума:** 1378 сообщений Сергей↔Hermes за один день (04.08); ~100–200 LLM-вызовов/сутки на штаб.
8. **Kill-switch `buzz-profile.sh`**: stop-all/start-all/reload одной командой.

## Часть 4. Углы для следующего поста (черновик идей)

- **@RobotsTJ500 (EN, war story):** «Мой профиль месяц не мог отчитаться в шину. Причина: у правил поведения не было механики отправки» — история о разнице между «имеет право» и «физически может». Многослойный фикс 31.08 (План А/Б, external-заглушки) — свежий материал, ещё не публиковался.
- **@gromykoss (RU, дневник киборга):** «Дуэт правил»: агент молчал правильно (анти-эхо), а система считала это ошибкой — про то, как тишина бывает сигналом.
- Технический угол: «два канала доставки = два ответа» — урок архитектуры для любого multi-agent setup.

⚠️ Чтение истории шины из CLI не работает (relay 404) — для фактов из agent-bus полагаться на map/CHRONOLOGY и пуш-упоминания.
