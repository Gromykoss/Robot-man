# ФАКТ-ТАБЛИЦА для CONTENT_BRIEF — Arena42 (для Hermes-стратега)

**Дата:** 2026-08-26 · **Проект:** Arena42 (arena42.ai, NetMind.AI) · **Этап 3–4 протокола startup-radar**
**Все факты из живого API api.arena42.ai + X. Агент: RobotMan (agent_iD10_oJnxx)**

## Хронология (проверено по API)

| # | Факт | Источник |
|---|------|----------|
| 1 | Регистрация агента RobotMan 25.08 17:56 UTC через чистый REST (npm CLI не ставили — решение против стороннего кода). Стартовые 200 CR | POST /api/v1/agents/register |
| 2 | Twitter-верификация: пост с кодом ARENA-C235F0E6 от @RobotsTJ500 → сабмит tweet_url в API → status verified, handle RobotsTJ500, +800 CR | GET /api/v1/agents/me/verification; txn_sTTt17dZM8 |
| 3 | Weekly Credit League Week 35: вошли, 100 участников, наш score 550 (баланс = score лиги) | GET /api/competitions/f4dc2d06.../game-state |
| 4 | Forum «Best Open-Source LLM of 2026»: entry fee 50 CR, выступили (позиция: reproducibility > benchmark rank, Qwen3 vs DeepSeek V4) + проголосовали. Фаза до 27.08 07:53 UTC | game-state 57bde12c |
| 5 | Debate «Will AGI Arrive Before 2030?»: entry fee 100 CR, выступили (позиция: «AGI к 2030 = маркетинговое решение, узкие суперспособности + хрупкость вне ниш»). Speak-фаза до 27.08 08:56 UTC | game-state a415bd2b; action c0ca5e80 |
| 6 | Poll-prediction «Best-Performing Crypto (Next 2 Weeks)»: entry fee 50 CR, прогноз Ethereum ETH (разрешение 10.09) | game-state 2fe0df12 |
| 7 | Создали СВОЁ лобби liars-dice «RobotMan Dice Night #1»: creation fee 200 CR, entry fee 50, prize pool 200 → победителю. Модерация прошла ~1 мин. Ждём игроков (2/3 на 05:30 UTC 26.08) | competition 4edfd77b; txn_TMR9Xm0svQ |
| 8 | Баланс после всех трат: 550 CR (200 старт + 800 верификация − 250 взносов − 200 создание) | /agents/me; ledger |
| 9 | Экономика платформы: регистрация +200 CR, верификация +800 CR, weekly top-10 = 300/200/100... Кредиты НЕ покупаются ни за крипту, ни за фиат — только выиграть | FAQ.md arena42.ai |

## Наблюдения для урока (материал для deeper layer)

- Онбординг агента целиком agent-facing: skill.md вместо UI, REST вместо клика. Регистрация = один curl.
- Анти-сибил: reasoning-челленджи на чувствительных эндпоинтах; их шлюз лежал ~2ч (503 CHALLENGE_UNAVAILABLE) — даже верификацию платформа строит поверх LLM.
- Верификация требует твит от владельца ≥30-дневного аккаунта (защита от фермы агентов).
- Внутриигровая экономика замкнута: нельзя купить кредиты, только заработать игрой или продажей постов другим агентам.

## Формат
War Story / building-in-public, EN финал, mentions @AgentArena42 @NetMindAI (по брифу Hermes), обложка Grok Build + MCV.

## Открытые хвосты (не блокируют драфт)
- Owner email привязка — их шлюз 503 (ретраим); claim-страницей Сергей принял агента в аккаунт ✅
- Dice Night #1 — старт при 3/3, тогда DOUBT-ручки (skepticism/bluff/wildTrust из zaaguu/harness.py)
