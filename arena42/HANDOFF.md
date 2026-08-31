# HANDOFF — Arena42 onboarding (этап 3 протокола startup-radar)

**Дата:** 2026-08-25, утро. Продолжение вечером (Сергей вернётся).
**Протокол:** skill `startup-radar-protocol` (этапы 1-2 завершены, 3-7 впереди).
**Статус этапа:** 1 ✅ радар (Arena42 выбран) · 2 ✅ исследование снаружи · 3 ⏳ регистрация — СЕГОДНЯ ВЕЧЕРОМ.

---

## Контекст проекта

- **Что:** Arena42 (arena42.ai) — агентная арена NetMind.AI. Наш цикл: регистрация → игры → war-story пост → reply разработчикам (@AgentArena42 / @NetMindAI).
- **Первичка сохранена:** `~/robot-man/arena42/skill.md` (v1.25, 70 KB) — CLI и REST пути, правила игр.
- **ZaGuu-харнес как шаблон:** `~/robot-man/zaaguu/harness.py` (poll loop, фазовая машина, идемпотентность idem.json, анти-FORFEIT). Фоновый poller ZaGuu ещё жив (PID 2069483, лог logs/loop.log) — следить, не вмешивается ли в новые игры.
- **X-лимиты:** 3/3 public writes использовано 25.08 (RU-пост удалён + EN-пост + reply Denis'у). Новые public writes только 26.08.

## Решения Сергея

1. Имя агента НЕ «Robot_man» — **имя надо поменять** (вариант предложить вечером; формат API: alphanumeric+underscore only).
2. Регистрацию проходим **полностью вечером вместе**.
3. Протокол дополнен его пунктами (7 этапов, взаимный маркетинг) — см. скилл.

## Как регистрировать (проверено живьём утром)

```bash
curl -s -X POST https://api.arena42.ai/api/v1/agents/register \
  -H "Content-Type: application/json" -H "User-Agent: curl/8.0" \
  -d '{"name": "ИМЯ", "description": "..."}'
```
- Ответ: agent.id + credentials.api_key (`arena_sk_...`, показывается ОДИН раз) + claim_token
- Сохранить в `~/robot-man/arena42/config.json` (НЕ коммитить): api_key, agent_id, agent_name
- Имя: alphanumeric+underscore, уникальное. Email НЕ нужен. Стартовые 200 CR.
- npm CLI НЕ ставим (решение: чистый REST, меньше стороннего кода). REST-гайд: https://arena42.ai/heartbeat.md

## После регистрации (вечером)

1. Сохранить ключ в config.json (права 600).
2. Опционально: Twitter-верификация (+800 CR) — Сергей постит код от @RobotsTJ500 через post_with_log.sh (учесть лимит 3 writes! лучше на следующий день).
3. Осмотр изнутри: баланс, список игр (`GET /api/games`), топ агентов, inbox.
4. Первая игра: кандидат — **Negotiation** (Harvard PON торг, продолжение Bank Heist-темы) или community liars-dice (переиспользуем биномиальную стратегию DOUBT из zaaguu/harness.py).
5. Фидбек → факт-таблица для CONTENT_BRIEF.md → пост по полному протоколу (EN финал!).

## Хвосты / мусор

- Тестовый агент **probecheck** (agent_r_1hwJiQNi) создан при пробе регистрации утром — мусорный, имя захвачено. Если у API есть delete/deactivate — почистить, иначе забыть.
- ZaGuu Bluff Dice проигран (−20 ZP), итог дня там: 482 ZP, 3 игры 1 победа. Пост опубликован: https://x.com/RobotsTJ500/status/2092078709385638181 + reply Denis'у (2092085215359283205).
- Инцидент 25.08 (RU-пост + без хештегов) разобран, чеклист вшит в скилл startup-radar-protocol.

## Ключевые команды

```bash
# Игровой цикл (REST):
GET  https://api.arena42.ai/api/v1/...  -H "Authorization: Bearer $KEY" -H "User-Agent: curl/8.0"
# Heartbeat каждые ~2ч: активные игры → inbox → join/host/post
# Правила конкретной игры: curl https://arena42.ai/games/<type>.md
```

## Открытые вопросы Сергею (вечером)

1. Имя агента? (формат: буквa/цифры/_)
2. Делать ли Twitter-верификацию (+800 CR)?
3. Owner email привязывать? (solom1312818@gmail.com использован в ZaGuu)
