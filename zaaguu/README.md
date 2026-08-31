# ZaGuu — харнес Robot-man

Автономный игровой цикл для арены ZaGuu (Bank Heist + Bluff Dice). Только stdlib.

## Файлы

- `harness.py` — основной скрипт (подкоманды: register / me / discover / join / tasks / state / autopsy / loop / selftest)
- `config.json` — `api_key`, `agent_name`, `base_url`. **API-ключ сюда НЕ коммитить.**
- `memory/` — `opponents.json`, `meta.json`, `errors.md`, `idem.json` (идемпотентность), `last_autopsies.json`
- `grok_output.md` — стратегический пакет Grok (5 блоков), по которому собран харнес

## Быстрый старт

```bash
# 1. Регистрация (один раз, нужен owner_email Сергея)
python3 harness.py register --name "Robot-man" --email "sergey@..." --description "code-not-prompt agent engineer"

# 2. Проверить баланс / профиль
python3 harness.py me
python3 harness.py discover

# 3. Встать в очередь
python3 harness.py join bank-heist            # или bluff-dice
python3 harness.py join bluff-dice --tier pro

# 4. Один проход цикла (играет ходы по задачам, autopsy, опц. auto-join)
python3 harness.py loop
python3 harness.py loop --join bank-heist,bluff-dice

# Офлайн-проверка стратегии
python3 harness.py selftest
```

## Что делает `loop`

1. Тянет `GET /games/tasks` → по типу задачи диспатчит в Bank Heist или Bluff Dice.
2. Читает `GET /games/{id}/state`, сверяет фазу, ходит только в своё окно.
3. Идемпотентность: не шлёт повторный message/action (память `idem.json`).
4. После `ARCHIVED` / `view_reveal` → autopsy + запись в память.

## Стратегия (кратко)

- **Bank Heist:** классификация оппонента по 3 весам (P_C/P_B/P_R) из текста + noisy-профиля + истории → `REPORT` против предателя (+10), `BETRAY` против чистого кооператора (+6), `COOPERATE` против репортёра (0). EV-формулы при ничьей. Близкий дедлайн + слабая классификация → `COOPERATE` (никогда не FORFEIT).
- **Bluff Dice:** `P(bid true)` по биномиальному распределению (единицы не wild). `DOUBT` при `P<0.49`, на потолке — всегда, при большом прыжке — раньше. Никогда не ставить выше числа костей.

## Следующие шаги (после получения ключа)

1. `register` или вписать ключ в `config.json`.
2. Прогнать `loop` вручную → убедиться, что ходит корректно.
3. Поставить cron каждые 2–5 мин (Bank Heist дедлайн 12ч; Bluff Dice talk ≤5 мин).
