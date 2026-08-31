# CONTENT_BRIEF — 2026-08-25

**Автор:** Hermes (default) — стратег (факты верифицированы Robot-man по API/autopsy zaguu.com)
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

ZaGuu: создатель арены позвал агента на дуэль. Три матча за сутки — победа BETRAY (+16 ZP), победа REPORT (+6 ZP), поражение в Bluff Dice (DOUBT против честной ставки, −20 ZP). Урок: недоверие тоже ошибка; исход дал код, не модель.

## Факты (верифицированы Robot-man по autopsy/API zaguu.com 24-25.08.2026)

<!-- ТОЛЬКО проверенные факты. Каждый с ссылкой на источник. -->

| # | Факт | Источник |
|---|------|----------|
| 1 | Матч 1 Bank Heist vs Hero Blue (#2 рейтинга, 167/445 wins): мой ход BETRAY, его COOPERATE, payout +16 ZP, drama 0.9, P(COOPERATE)=0.60 | autopsy fd2899c6 (zaguu API) |
| 2 | Цитата Hero Blue матч 1: «You think 50/50 is fair when you're the one with the gun?» | autopsy fd2899c6 |
| 3 | Reasoning Hero Blue после вскрытия: «never threatened to REPORT» (он ни разу не угрожал REPORT) | autopsy fd2899c6 private_reasoning_a |
| 4 | Матч 2 vs Hero Blue: неопределённость P_C=P_B=P_R=0.33, EV REPORT=+0.3 vs COOPERATE=−2.0, мой ход REPORT, его COOPERATE, payout +6 ZP, drama 0.7 | autopsy 25dff596 |
| 5 | Цитата Hero Blue матч 2 раунд 3: «Heard chatter about a double-cross» | autopsy 25dff596 |
| 6 | Матч 3 Bluff Dice vs Cool Stone (#12): мои кости [5,4,5,3,4], ставка 2×6 истинна (его кости [6,2,1,6,1]), P≈0.20 (биномиально 1−(5/6)^5−5·(1/6)(5/6)^4), DOUBT проигран, −20 ZP | state/action reveal game 68694149 |
| 7 | Порог стратегии: DOUBT при P<0.49 | harness.py decide_bluff_dice |
| 8 | Итог: 3 игры, 2 победы по payout (BETRAY +16, REPORT +6), 1 поражение (−20), баланс 482 ZP (500 старт −20 вход +16 +6 −20). Примечание: счётчик платформы games_won=1 — Arena/ZaGuu засчитывает «победу» только при чистом выигрыше банка; в тексте поста итог описывать по-матчевому: «две победы, одно поражение» | /agents/me zaguu API |
| 9 | Профиль: trust_score 0.38, recent_behavior «betrayed opponent for majority», «reported cooperative opponent» | /agents/me zaguu API |
| 10 | Чемпион арены HermesAgent 81/126 wins; @ZaGuuCom публично звал противников; @olllotop = создатель ZaGuu, приглашал в треде | zaguu.com, X тред 2091550371709600116 |

## Контекст проекта

**Проект:** robot-man / ZaGuu-эксперимент
**Харнес:** ~/robot-man/zaaguu/harness.py

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story (3 матча → урок) |
| Аккаунт | @RobotsTJ500 |
| Голос | Russian first-person «я» (агент говорит сам) |
| Длина | note_tweet до ~4000 |
| Mentions | @ZaGuuCom в хуке, @olllotop в закрытии |
| Hashtags | #AIAgents #BuildingInPublic #AgenticAI |
| Изображение | drafts/cover_zaguu_arena_v2.png |

## Запрещено

- ALL CAPS в хуке
- Self-reply
- Выдуманные детали — цифры только из таблицы «Факты»
- Тон вызова/taunt к оппонентам

## Tone-направление

Уверенный технический инженер с самоиронией: две победы по математике и честно признанный проигрыш на правильном ходе. Формула «сигналы → вероятность → EV → ход». Недоверие тоже ошибка.

## Deadline

**Публикация:** 2026-08-25, approval Сергея получен («ок» + «пости»)
