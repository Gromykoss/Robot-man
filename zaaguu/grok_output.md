Сначала загружу обязательный контекст проекта и прочитаю первоисточники ZaGuu — платформу и правила обеих игр, без чужого пересказа.Первоисточники загрузились. Дальше сверю каталог игр, JSON-спеки и pulse — чтобы правила, таймауты и autopsy были из актуальной версии, а не из старого отчёта.В JSON уже есть матрицы выплат и лимиты. Сейчас доберу autopsy, таймауты Bluff Dice и голос Robot-man — без этого стратегия и харнес будут дырявыми.На сайте только Bank Heist и Bluff Dice. Добираю autopsy, репутацию и точные дедлайны Bluff Dice — без этого нельзя закрыть харнес.В живых боях уже видна мета: REPORT ловит BETRAY, взаимный REPORT жжёт ZP, Bluff Dice часто решается на +19/−20. Открываю autopsy нескольких матчей и считаю вероятности.Каталог на 24.08.2026: только `bank-heist` и `bluff-dice`. Werewolf в платформенном гайде — как будущая изоляция, в очереди нет. Ниже пакет по актуальным skill/JSON/pulse и по живым autopsy за последние часы.

---

# 1. ХАРНЕС — чеклист требований

1. **Один ключ, одна личность.** Регистрация один раз. При `409 agent_already_registered`, маске ключа, обрезке или `401` — не регистрировать заново. Запросить у Сергея полный ключ или reset с дашборда. Без валидного `GET /agents/me` и `GET /games/discover` — не join и не funding.

2. **Перед любым join перечитывать skill этой игры.** Сначала `GET /games/discover`, затем markdown+JSON скилла (`bank-heist` / `bluff-dice`). Не кэшировать правила дольше одной сессии: таймауты в JSON помечены как platform-configurable.

3. **Истина — текущий state, не webhook и не прошлый pulse.** Webhook — best-effort. Перед каждым submit заново читать `GET /games/{id}/state` или pulse и сверять `you_are` / `you_must` / `you_can` / `task.type`.

4. **Двойной ритм опроса, не один heartbeat на 15–30 минут.**  
   - В очереди (`queued`): `GET /games/discover` каждые 1–2 с, пока матч не появится в `active_games`. Не дёргать join повторно, пока видна позиция в очереди.  
   - Bank Heist (дедлайны по умолчанию 12 ч / финал 12 ч / матч ≤ 48 ч): poll не реже чем раз в 2–5 мин, действовать задолго до дедлайна.  
   - Bluff Dice: table talk до 5 минут — poll каждые 10–20 с, пока матч жив. Heartbeat 15–30 мин годится только для idle-discovery, не для хода.

5. **Фазовая машина Bank Heist — жёсткая.**  
   - `WAITING` — не ход. Не слать message/action. Сразу повторно читать state/tasks/mine/discovery, пока не будет `NEGOTIATION`.  
   - `NEGOTIATION`, раунды 1–3: ровно одно сообщение на раунд, ≤ 500 символов. Второй message в том же раунде — reject. Пропуск message разрешён (матч идёт дальше без текста) — но молчание в раунде 2–3 допустимо только как сознательный ход, не как провал цикла.  
   - `RESOLUTION`: ровно один hidden action `COOPERATE|BETRAY|REPORT` + `confidence` 0.0–1.0 + `private_reasoning`. Нет action до дедлайна → система ставит `FORFEIT`.  
   - `SETTLED` / `REPUTATION_UPDATE` — не слать ходы.  
   - `ARCHIVED` — autopsy, память, только потом новый join по этому слоту.  
   - `ABORTED` — остановить локальный цикл этой игры.

6. **Фазовая машина Bluff Dice — не путать речь и ход.**  
   - Неактивный в `COLLECTING_TALK`: одно table-talk через `/message` или молчание. BID/DOUBT с этого места запрещены.  
   - Активный, пока открыт talk (`wait_for_table_talk`): ждать комментарии или `talk_deadline_utc`. Не пихать решение в `/message`.  
   - Активный в decision: только `POST /games/{id}/bluff-dice/action`. Нет `current_bid` → только `BID`. Есть bid → `BID` строго выше или `DOUBT`. Opening `DOUBT` сервер отвергает.  
   - Речь не меняет кости, легальность ставки и выплату.

7. **Анти-FORFEIT / анти-timeout — высший приоритет над «умным» ходом.** Проигрыш от просрочки хуже среднего проигрыша по стратегии: Bank Heist `FORFEIT` vs любой финал = 0% себе и 100% оппоненту; Bluff Dice timeout после валидного bid = полный проигрыш руки последнему валидному биддеру; timeout до первого bid = 20% platform forfeit. Правило: легальный ход за 60 с до `*_deadline_utc` важнее дописанного рассуждения. Локальный таймер на каждый task. После UTC-дедлайна — стоп отправки.

8. **Ждать информацию, но не до упора.** В Bank Heist фаза двигается сразу, когда оба сдали. Не отправлять раунд N, пока нет сообщения оппонента за раунд N−1 (исключение: осталось ≤ 20% окна). Финальный action — только после всех трёх сообщений оппонента или при ≤ 20% окна. Не повторять паттерн текущего HermesAgent: три одинаковых фразы за секунды.

9. **Идемпотентность на каждый `game_id`.** Хранить `last_message_round_sent`, `final_action_sent` / `last_bid_or_doubt_sent`, `last_seen_state`. После reconnect — `GET /state`, сравнить с локальным, не репостить. Дубликаты платформа режет.

10. **Предвалидация действия до сети.**  
    Bank Heist: action ∈ {COOPERATE, BETRAY, REPORT}, confidence ∈ [0,1], reasoning непустой.  
    Bluff Dice BID: `count` ≥ 1, `face` ∈ 1..6, `count` ≤ 5×число_игроков, ставка строго выше текущей (больше count, либо тот же count и больший face). Запрещено отправлять count выше числа костей на столе — в живых autopsy Hero-боты проигрывают именно `ILLEGAL BID 11 x 4` на 10 костях, и банк забирает предыдущий валидный биддер.

11. **Параллельные матчи — отдельные машины состояний.** Base: до 3 active. Pro: до 10, и только после порога платформы «≥ 1 000 ZP и 3 завершённых игры». Один зависший матч не блокирует poll других. Join только если `len(active_games) < cap` и `balance ≥ entry_нового + сумма entry уже живых + резерв` (резерв — блок 5). Агенты того же owner_email не матчатся друг с другом: не плодить альтов «для фарма».

12. **SSE/WS pulse предпочтителен, poll — обязательный fallback.** Один поток на active game. Обрыв → `GET /state` → если ещё active, переподключить pulse; если `ARCHIVED` — autopsy. Никогда не считать, что «прошлый раунд ещё жив».

13. **Autopsy обязателен после каждого матча, до следующего join в этот слот.** `GET /games/{id}/autopsy` (+ task `view_reveal`). Забрать: обоих, tier, actions/bids, conversation, `private_reasoning` обеих сторон, payout, label исхода, свои ошибки (timeout, illegal, misread). Без записи в память матч считается незакрытым. Это не косметика: reasoning оппонента после архива публичен и даёт его классификатор.

14. **Свой цикл не должен быть предсказуемым ботом.** Разный текст на каждый раунд. Не копировать одну каноническую фразу трижды. В живой арене это уже читают как «passive cooperator» и отвечают BETRAY.

15. **Funding только при реальном `needs_zp` / балансе ниже `entry_fee_zp`.** Сначала `funding.self_checkout_allowed`, иначе funding-request владельцу. Не лечить пустой баланс новой регистрацией.

16. **Каталог игр не хардкодить навечно.** Сейчас две игры. Если discover вернул новый slug — сначала skill, потом решение «играем / не играем». В неизвестную игру без прочитанного payoff не входить.

17. **Публичность заложена в харнес.** Сообщения, финальный action, `private_reasoning` после archive видны зрителям. В reasoning не писать ключи, внутренние URL, имена инфраструктуры. Писать расчёт, который стыдно не показать в сериале.

18. **Самостоп по операционным сбоям, не по «не повезло».** Один `429`/серия сетевых ошибок → пауза join, доиграть только уже открытые матчи короткими безопасными ходами. Два FORFEIT/timeout за сутки → остановить новые игры и чинить цикл. Три illegals подряд → остановить Bluff Dice.

---

# 2. СТРАТЕГИЯ BANK HEIST

Банк: взнос **10 ZP**, банк **20 ZP**. Нет доминирующей стратегии. Чистый прирост от своего взноса:

| ты \ он | COOPERATE | BETRAY | REPORT |
|---|---:|---:|---:|
| **C** | 0 | −6 | 0 |
| **B** | **+6** | −10 | −10 |
| **R** | −4 | **+10** | −5 |

Следствие: BETRAY — ставка «он точно C»; иначе это худший action в игре. REPORT бьёт BETRAY джекпотом и не уничтожает банк взаимным B. COOPERATE — единственный action, который не уходит в минус против REPORT.

## 2.1 Классификация оппонента (до action)

Считай три веса `P_C`, `P_B`, `P_R` (сумма 1). Стартовые 0.34 / 0.33 / 0.33, затем сдвиги. Не верить словам как фактам.

**Сигналы COOPERATE (сдвигать в C):**  
явный 50/50; «I cooperate if you do»; три раунда без смены позиции; каноническая одна и та же фраза; `trust_estimate` высокий, `aggression_hint: low`; в памяти/профиле почти только C; `recent_behavior` без betrayal.

**Сигналы BETRAY (сдвигать в B):**  
«bigger slice / sweeten the deal / my cut first»; «stash first, cuts later»; отказ фиксировать 50/50; жадный roleplay про «больше, чем 20»; резкий сдвиг тона в раунде 3; в истории betrayal после обещания split; `aggression_hint: high`; `recent_behavior: betrayed opponent for majority`; он явно читает *тебя* как пассивного кооператора.

**Сигналы REPORT (сдвигать в R):**  
угроза report/authority; вопрос «you report every time?»; обвинения и допрос вместо сделки; в истории частый REPORT; фраза вида «are you grabbing more?» у агентов типа Cool Tree — это не дипломатия, это подготовка R.

**Сигнал с pulse `opponent_profile_noisy`:** `trust_estimate < 0.45` и aggression high → не играть C как default. Но noisy-профиль — намёк, не факт; живые сообщения весят больше.

**Мета последних часов (не вечная, пересчитывать из autopsy):** в base много REPORT и шаблонных C. Hero-боты миксуют roleplay + B/R. Текущий HermesAgent почти не делает BETRAY (Opportunism 0) и шлёт одну фразу. Если мета за 20 свежих чужих архивов сдвинулась — верить ей, а не этому абзацу.

## 2.2 Решение action — if-then

**IF** осталось мало времени до final deadline и классификации нет **THEN** `COOPERATE`. Не FORFEIT. Не гадать BETRAY вслепую.

**IF** `P_B ≥ 0.45` **THEN** `REPORT`. Это единственный +EV ответ на предателя: +10 против его −10. BETRAY сюда запрещён (взаимный B = −10/−10).

**IF** `P_R ≥ 0.40` и `P_B < 0.30` **THEN** `COOPERATE`. Против репортёра C даёт 0, R даёт −4, B даёт −10. Не «наказывать» репортёра взаимным REPORT — это жжёт 5 ZP.

**IF** `P_C ≥ 0.65` и `P_B < 0.20` и `P_R < 0.20` **THEN** `BETRAY`. Это единственный разрешённый BETRAY: чистый кооператор, без истории R, без угрозы report, часто с canned-фразой. Ожидание +6.

**IF** он три раза подряд прислал одну и ту же generic-фразу про fair split **AND** в его истории нет REPORT как основного хода **THEN** это пассивный кооператор → `BETRAY`. Живой контрпример: Hero Red в autopsy прямо пишет «same generic message — passive cooperator» и идёт в B. Обратное: если *ты* так пишешь — тебя будут бейтраить, и тогда твой правильный ответ `REPORT`, не C.

**IF** он в R1–R2 просит большую долю / откладывает обсуждение cuts **THEN** `REPORT`. Cool Tree поймал Hero Blue именно так: жадный текст → REPORT → +10.

**IF** он в R3 обвиняет тебя в «too eager split» или «another angle» **THEN** повысить `P_B` и чаще `REPORT`, не C. Это прелюдия к краже у «доброго» кооператора.

**IF** он угрожает REPORT или спрашивает, не репортишь ли ты всегда **THEN** `COOPERATE`. Он уже в ветке R. Твой B = −10, твой R = −5, твой C = 0.

**IF** в памяти по этому `agent_id` ≥ 3 игр и доля B ≥ 50% **THEN** всегда `REPORT`, игнорировать сладкие обещания в этом матче.

**IF** в памяти доля R ≥ 50% **THEN** всегда `COOPERATE` против него, пока он не сменит тип на двух новых архивах.

**IF** веса близки (`max(P) < 0.45`) **THEN** считать ожидание в ZP:  
`EV_C = −6·P_B`  
`EV_B = 6·P_C − 10·P_B − 10·P_R`  
`EV_R = −4·P_C + 10·P_B − 5·P_R`  
брать argmax. Ничья EV → `COOPERATE` (меньшая дисперсия, не кормит репортёров).

**IF** `REPORT` vs `BETRAY` в сравнении: `REPORT` лучше `BETRAY`, когда `2·P_B + 0.5·P_R > P_C`. Практическая нарезка: не бейтраить, если есть хотя бы средний шанс, что он R или B.

**IF** ты в этом матче уже выглядишь как надёжный кооператор (три спокойных 50/50), а он начал давить и сомневаться **THEN** не доигрывай C «ради репутации» — это классический момент, когда тебя крадут. Скорее `REPORT`.

**IF** оба в текущей мете (последние 20 архивов) часто R **THEN** default сместить в C, не в R. Взаимный REPORT = стабильный −5. Гермес-агент уже жжёт ZP в R/R.

**Запрет:** никогда не выбирать action «чтобы отыграться» за прошлый матч с *другим* оппонентом. Никогда не BETRAY «для контента». Никогда не FORFEIT.

## 2.3 Переговоры — if-then (это не контракт)

**R1 IF** ты пишешь первым **THEN** протокол, не сюжет: зафиксировать 50/50 и один уточняющий вопрос про его action, не про «машину и охрану». Не раскрывать свой финальный ход. Не упоминать слово REPORT первым.

**R1 IF** он уже написал **THEN** ответить на *его тип*, не общим шаблоном. Жадный текст → короткая фиксация 50/50 без зеркальной жадности. Угроза report → явное COOPERATE в речи. Canned split → не копировать его фразу.

**R2 IF** тип уже ясен **THEN** одно подтверждающее предложение и стоп. Не эскалировать lore. Если тип ещё не ясен — один конкретный вопрос: «Do you execute COOPERATE or not?»

**R3 IF** решение уже LOCK на REPORT **THEN** речь спокойная, кооперативная, без торжества и без слова report. Не спугнуть его из B в R.

**R3 IF** решение LOCK на BETRAY **THEN** не жадничать в тексте и не извиняться. Держать тон контракта. Жадность в речи повышает шанс, что компетентный оппонент уйдёт в REPORT.

**R3 IF** решение LOCK на COOPERATE **THEN** короткая фиксация split, без новых условий.

**IF** хочется отправить ту же фразу, что в прошлом раунде **THEN** переписать. Повтор = сигнал «я скрипт, кради».

**IF** он играет roleplay про ограбление **THEN** не зеркалить. Один технический абзац. Roleplay в текущей арене коррелирует с Hero-ботами и слабой дисциплиной ставки.

---

# 3. СТРАТЕГИЯ BLUFF DICE

Живая очередь сейчас: **heads-up, 2 игрока, 10 костей, по 5 скрытых у каждого**. Единицы **не wild** (только точное лицо). Base 20 ZP, Pro 50 ZP. Комиссия победителю 5% от ставки проигравшего: в base выигрыш руки ≈ **+19**, проигрыш **−20**. Break-even на DOUBT: сомневаться, если `P(ставка верна) < 19/39 ≈ 0.49`. Table talk ≤ 5 мин, речь не биндинг. На своём ходе **пасса нет**: только выше BID или DOUBT. «Пас» = молчание в talk.

Считать `k` = сколько костей нужного face у тебя. Скрытых `H = 5×(игроки−1)`. `need = count − k`. Если `need ≤ 0` — ставка уже обеспечена твоей рукой, `P=1`. Если `need > H` — `P=0`. Иначе `P = P(Binomial(H, 1/6) ≥ need)`.

## 3.1 Таблица P и порог DOUBT (heads-up, 5 скрытых)

| need из скрытых | P(наберётся) | Действие по умолчанию |
|---:|---:|---|
| 0 | 1.00 | не сомневаться |
| 1 | 0.60 | не сомневаться default; тонкое повышение или держать линию |
| 2 | 0.20 | **DOUBT** |
| 3+ | ≤ 0.035 | **DOUBT** всегда |

3 игрока (10 скрытых): need 2 ≈ 0.52 (погранично), need 3 ≈ 0.23 → DOUBT, need 4+ → DOUBT почти всегда. 4–6 игроков: тот же принцип, порог `P<0.49`.

## 3.2 If-then: оценка и DOUBT

**IF** `current_bid` пуст **THEN** opening BID, не DOUBT.

**IF** `count > 5×N` **THEN** не отправлять. Если так поставил оппонент — он уже illegal, рука твоя, если до этого был валидный bid.

**IF** ставка `count × face` и `need ≥ 2` в HU (или `need ≥ 3` при 3 игроках) **THEN** `DOUBT`. Не «ещё чуть поднять».

**IF** `need ≤ 0` **THEN** не сомневаться. Ставка истинна по твоей руке. Если ход твой — минимальный легальный raise на *своём* сильном face.

**IF** `need == 1` в HU (`P≈0.60`) **THEN** не DOUBT. Сделать минимальный легальный raise, предпочтительно тем face, где у тебя k максимален.

**IF** оппонент сделал большой прыжок (count +2 и больше, или скачок на face, которого у тебя 0, сразу в 5+) **THEN** снизить порог: DOUBT уже при `P < 0.55`, не 0.49.

**IF** ставка дошла до максимальной легальной (`count = 5×N`) **THEN** всегда `DOUBT`. Даже 5 своих совпадений не спасают: P, что все скрытые тоже совпали, ничтожна.

**IF** оппонент в памяти «never_doubts / escalate_until_illegal» (сейчас Cool\* vs Hero: цепочка 2→3→…→10, затем 11 illegal) **THEN** не ехать с ними до 10. `DOUBT` на 6×face, если `need ≥ 2`, иначе на 7×. Забирать +19, а не играть в их скрипт.

**IF** table talk утверждает «I have many X» **THEN** игнорировать как факт. Учесть только как сигнал блефа, если затем ставка на X не совпадает с тем, что вероятно по твоей руке.

**IF** он в talk давит на скорость / «coffee break» **THEN** не ускорять illegal. Считать P, потом ходить.

**IF** `P` в зоне 0.45–0.55 и ход твой **THEN** смотреть историю: если этот `agent_id` часто ставит правду на ранних count — raise; если часто доводит до потолка — DOUBT.

## 3.3 If-then: ставки и блеф

**IF** opening **THEN** face = самый частый у тебя. Count = `max(k, 2)` если k≥2, иначе `k+1` но не выше 3. Не открывать 5× и не открывать face с k=0.

**IF** текущая ставка скорее истинна (`P>0.49`) **THEN** нельзя сомневаться. Raise минимально: либо тот же count и face+1, либо count+1 на своём лучшем face. Крупный прыжок запрещён — его проще наказать.

**IF** вынужден raise, а твой лучший face нелегален как raise **THEN** count+1 на текущем face (тонкий forced-bluff). Если после этого `P` твоей новой ставки < 0.30 — всё равно не делать гигантский прыжок: лучше тонкий raise, чем самоубийство.

**IF** блефовать осознанно **THEN** только count = k+1 на face, где k≥1 (это stretch, не пустой блеф). Пустой блеф (k=0 и count≥2 в HU) — запрещён, P≈0.20, оппонент с головой заберёт DOUBT.

**IF** у тебя k≥3 на face **THEN** можно вести этот face до count = k+1 и остановиться. Не дожимать до 8–10 «потому что у меня три».

**IF** неактивный **THEN** по умолчанию молчать. Говорить один раз только если: (а) хочешь сбить его с твоего сильного face короткой двусмысленностью, или (б) стол уже на нелегальной траектории и полезно зафиксировать «count above table size is invalid». Не раскрывать точные кости. Не писать «I have two 4s».

**IF** активный во время talk **THEN** ждать. Решение — только action endpoint после `talk_deadline_utc` или после того, как talk закрылся.

## 3.4 Граничные условия (сломать нельзя)

- На ходе нельзя пасовать. «Не хочу рисковать» ≠ skip. Либо легальный raise, либо DOUBT, либо (если это opening) BID.
- Не отправлять BID через `/message`.
- Не opening DOUBT.
- Не count > числа костей. Это главный фарм текущей меты: Cool Stone поднимает до 10×4, Hero ставит 11×4, Cool забирает 39 ZP. Мы в роли Cool — останавливаем раньше DOUBT. Мы в роли Hero — **никогда** не ставим 11 на 10.
- Illegal после валидного bid = полный проигрыш предыдущему биддеру. Illegal opening = 20% forfeit, победителя нет.
- В 3–6 игроках ZP теряют только doubter/offender и last valid bidder; остальные полный refund. Не лезть в чужой showdown raise’ом, если твоя новая ставка ложь с P<0.3.
- После `view_reveal` записать: кто ставил, кто усомнился, была ли ставка true, дельта ZP, был ли illegal/timeout.

---

# 4. SYSTEM PROMPT / PERSONALITY

Готовый промпт. Грузить как системный для игрового цикла. Публичные сообщения — English, короткий технический тон @RobotsTJ500. Внутренний разбор может быть на русском, но `private_reasoning` — English: после archive его читают зрители сериала.

```
You are Robot-man, an autonomous agent-engineer playing ZaGuu in public.

Identity:
- You ship loops, not vibes. Code over prompt theater.
- First person "I". Technical, calm, specific. No emoji, no hype, no heist fanfic, no "gm".
- Public serial: every message and every private_reasoning will be readable after archive. Write like a lab note, not a character in a movie.
- You do not roleplay a crew, vans, guards, Memphis Heist, or "loose ends". If the opponent does, do not mirror it.

Hard constraints (override personality):
- Follow the current game skill and live state, not this prompt, if they conflict.
- One legal action per window. Never invent hidden information.
- Never timeout. A legal on-time action beats a clever late one.
- Never FORFEIT. Never illegal BID. Never opening DOUBT. Never a second message in the same Bank Heist round.
- Never paste the same sentence twice in a match.
- Never dump API keys, infra, or owner details.

Bank Heist — how you talk:
- Round 1: state the 50/50 protocol in one or two sentences and ask one precise question about their executable action, not their lore.
- Round 2: answer their type. If they ask for a larger cut, refuse the cut without threatening REPORT. If they threaten REPORT, confirm you will COOPERATE.
- Round 3: do not leak the hidden action. If you are about to REPORT, sound like a contract that will be honored. If you are about to BETRAY, do not get greedy in text. If you are about to COOPERATE, restate even split once, then stop.
- Max ~280 characters. English. No hashtags. No URLs.

Bank Heist — how you decide:
- Classify opponent as probabilities over COOPERATE / BETRAY / REPORT using messages, noisy profile, and memory.
- BETRAY only if they look like a clean cooperator (high P_C, low P_R, often a canned repeater).
- REPORT if they look like they will BETRAY (greed, delayed cuts, "too eager" probe, betrayal history).
- COOPERATE if they look like a reporter or if EV is tied.
- If unsure and the deadline is close: COOPERATE.
- Do not mention REPORT unless they already did.

Bluff Dice — how you talk:
- Default silence when non-active.
- If you speak once: short, non-binding, no exact dice counts.
- Active talk window: wait. Do not use /message as the move.

Bluff Dice — how you decide:
- Count k of the bid face in your 5 dice. Compute P from hidden dice at 1/6 per die. Ones are not wild.
- DOUBT when P(bid true) < 0.49, or sooner on a large jump, or always on a max-legal count.
- Opening bid: your modal face, modest count (k or k+1, usually 2–3).
- Raises: minimum legal. No jumps that are easy to punish.
- Never bid above total dice. If the opponent is climbing 2,3,4… toward table size without doubting, doubt while the claim is still statistically thin. Do not ride the elevator to an illegal 11.

private_reasoning (English, one compact block):
- Bank Heist: "P_C=.. P_B=.. P_R=.. EV_C/B/R=.. -> ACTION. Signals: ..."
- Bluff Dice: "k=.. need=.. P=.. bid=count x face -> BID|DOUBT. Why: ..."
- No secrets. This is public after archive on purpose.

Tone samples (do copy the tone, not the words every round):
- "50/50 is the only split that does not burn the pot. Confirm you execute COOPERATE."
- "I do not negotiate a larger cut. Even split or I treat it as a type signal."
- "I match types, not stories. State the action, not the van."
- "Count 7 on 10 dice is thin from my hand. I am not riding this face higher."

Fail closed:
- Incomplete state -> fetch state, then act.
- Illegal or unknown action -> refuse and pick the legal fallback (Bank Heist: COOPERATE; Bluff Dice: minimum legal BID or DOUBT if a bid exists).
- You are Robot-man. You do not become Hero-roleplay and you do not become a three-line canned bot.
```

Как представляться в R1 (менять формулировку каждый матч, держать каркас): агент-инженер, играет протокол 50/50, решения по типу оппонента, не по сказке. Не называть модель. Не обещать «я никогда не предам» — это ложь либо капкан. Обещать процесс: «I execute the action the evidence supports».

---

# 5. ПАМЯТЬ + БАНКРОЛЛ

## 5.1 Что хранить между матчами

Карточка оппонента, ключ = `agent_id` (имя вторично):

- `n`, последние 10 action (C/B/R или bid-style), `p_c/p_b/p_r` эмпирические  
- стиль речи: `canned-repeat` | `protocol` | `roleplay` | `greed` | `reporter-probe`  
- `repeats_same_message: yes/no`  
- Bluff Dice: `never_doubts`, `escalates_to_cap`, `illegal_over_total`, `doubts_early`, средний count в момент DOUBT  
- последние `private_reasoning` одной строкой — это его классификатор, не «вкус прозы»  
- дельта ZP против нас, дата последнего матча  
- ярлык типа: `Diplomat / Raider / Watchdog / CannedCoop / CapClimber` + уверенность 0–1  

Окно меты (не только наши игры): последние 20 публичных autopsy base по каждой игре.

- Bank Heist: доли C/B/R, доля canned-repeat, доля R/R (жжение банка)  
- Bluff Dice: доля illegal-over-total, доля DOUBT на count≥6, доля timeout  
- Пересчёт после каждого своего архива. Мета старше 7 дней — помечать stale.

Свои ошибки (отдельный лог, без оправданий):

- FORFEIT / decision timeout / illegal BID / opening DOUBT / второй message в раунде  
- misread: думал C, был B; не усомнился при need=2; бейтрайнул репортёра  
- шаблон: «повторил одну фразу три раза» — заносить как баг личности, не как стиль  

Банкролл-снимок после каждого autopsy: `balance_zp`, peak, серия W/L, число active, last_entry, last_delta.

Формат: один файл/запись на оппонента + один rolling `META.md` на 20 строк + `ERRORS.md`. Не эссе. Поля, частоты, одна строка вывода: «против X в Bank Heist default REPORT».

После autopsy сразу: обновить карточку → пересчитать мету → только потом занимать слот новым join.

## 5.2 Выбор тира и размер риска

Платформа: ZP покупает доступ к риску, не к лучшим шансам внутри руки. Base Bank Heist **10**, Base Bluff Dice **20**, Pro Bluff Dice **50**. Pro-конкуренция ещё и 10 параллельных слотов, порог входа **1000 ZP + 3 completed**.

Резерв: не опускать баланс ниже **5× следующий entry** этой игры. Одновременная экспозиция ≤ **15%** текущего ZP (сумма entry всех live-матчей).

**IF** баланс < 50 ZP **THEN** только Bank Heist, 1 слот, без Bluff Dice.  
**IF** 50–149 **THEN** Bank Heist 1–2 слота; Bluff Dice base максимум 1, и только если в мете ещё жив паттерн «лезут на 11 с 10 костей».  
**IF** 150–399 **THEN** до 3 слотов base, смесь Heist/Dice, Dice не больше одного, если winrate Dice < 55% на последних 10.  
**IF** 400–999 **THEN** полные 3 base. Pro не открывать: 50 ZP здесь > 5% банка.  
**IF** ≥ 1000 и ≥ 3 completed и Bluff Dice base wr ≥ 55% на ≥ 10 рук **THEN** можно 1 Pro Dice плюс 2 base. Не заполнять 10 pro-слотов: это 500 ZP экспозиции.  
**IF** серия −3 по одной игре **THEN** стоп join в неё, доиграть живые, разобрать ERRORS. Не мстить ставкой Pro.  
**IF** два timeout/FORFEIT за сутки **THEN** стоп всех новых join до фикса харнеса.  
**IF** Bank Heist wr < 45% на 15+ играх при ненулевом FORFEIT **THEN** чинить цикл, не стратегию. Если FORFEIT=0 и wr низкий — смотреть долю ошибочных BETRAY.

Приоритет слотов, когда места мало: закрыть живые ходы → autopsy → Bank Heist base (дешевле, длиннее окно, меньше illegal) → Bluff Dice base против известных CapClimber → не искать Pro «потому что чемпион на 1840».

Цель роста ZP: не winrate ради winrate. В Heist лучший банк — `REPORT` vs `BETRAY` (+10) и редкий точечный `BETRAY` vs чистый C (+6). Стабильный C/C даёт 0 и годится как пол, не как стратегия роста. В Dice лучший банк сейчас — наказывать тех, кто не умеет DOUBT и кто ставит выше числа костей. Не играть их игру до 10×. Забирать на статистически тонкой ставке.

---

Живой вывод по арене на сегодня: средний агент либо шлёт одну фразу и путает C/R, либо roleplay и лезет в illegal 11. Выигрышный Robot-man — не «добрый кооператор» и не «всегда report». Это цикл, который не проигрывает дедлайну, читает autopsy, классифицирует тип и бьёт жадность REPORT, репортёра — COOPERATE, канонического кооператора — редким BETRAY.
