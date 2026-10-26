# MoA Рецензия 1 — качество + anti-ad («read-only credentials», v1, 26.10)

**Вердикт: CHANGES_REQUIRED** (1 блокирующий фикс: кредит @asifalis; остальное — PASS)

## 1. Voice — PASS с ремаркой
- First-person «I» выдержан в личных местах: «my replies», «my post», «Building in public» ✅
- Анти-попа: нет хайпа, нет восклицаний, нет «game-changer/revolutionary» ✅
- No ALL-CAPS в первых 160 символах ✅ («Banks banning agents from customer accounts…» — всё lowercase, акронимов нет)
- Ремарка: «Our fleet runs the same line» — «our» вместо «I». В голосе аккаунта флот описывался и так («our pipeline» в посте 24.10), допустимо, но если хотим жёсткого «I» — заменить на «My fleet». Не блокирующе.
- Честные минусы: explicit honest gap (human «ok» = control, not scope) — сильный, точный, без self-flagellation ✅

## 2. ⛔ ANTI-AD — PASS
- Нет лендингового тона, слоганов, CTA («follow», «check out», «try X» отсутствуют).
- «Building in public. 🤖» — фирменная подпись, не селл.
- Self-promo (наш fleet) подан после scar-контекста и рядом с honest gap — процедура соблюдена ✅
- Закрывающий абзац — тезис, не реклама.

## 3. ⛔ MENTIONS — **FAIL → фикс**
- Протокол: тезис-ядро поста принадлежит **@asifalis** (его формулировка «bank can cut off one agent without resetting the owner's password»). В тексте он обезличен: «an engineer left under my post». Это использование чужого тезиса без кредита — нарушение mention-credit gate.
  - **Фикс:** «…the reason fits in one sentence **@asifalis** left under my post: …»
- **@Plaid** — упомянут словами («like Plaid»), без @. Это допустимо и даже безопаснее (протагонист scoped-модели, не реклама), но по протоколу ожидался @Plaid. Оставить словами — ок; ставить @ не обязательно (не наш источник тезиса).
- Axios / USA Today — в тексте не названы вообще; факты (5 банков, CISO-доля) поданы как факт-база. Протокол разрешает «источники словами» — отсутствие упоминания приемлемо, но если хотим гигиены, можно «per Axios» во 2-м абзаце. Не блокирующе.
- @ProudCat98, @ReneChavez_wooo — по протоколу можно не упоминать ✅ (реплики парафразированы без атрибуции, что корректно для согласий; цитата «rent money at 3am» — Rene, подана как «the reactions in my replies», ок).

## 4. Пара текст+обложка — PASS
- Обложка: робот в закрытом банке с голографическим бейджем **READ ONLY** — метафора ровно главного тезиса (агенту разрешено смотреть, но не действовать; граница доступа) ✅
- Не дублирует хук дословно: хук — «watching and acting are different identities», на обложке только «READ ONLY» + «CLOSED» на окошках — усиливает, не повторяет ✅
- Логотипов, брендов, хендлов на обложке нет ✅
- Стиль (tech-noir, синий + зелёный) соответствует канону обложек.

## 5. Цифры — PASS
- 5 банков (Morgan Stanley, JPMorgan, BofA, Wells Fargo, Citi) — Axios ✅
- Two-thirds CISO — Palo Alto Networks 2026 / USA Today ✅
- «3am» — риторический образ из реплики, не статистика ✅
- Других чисел/статистики нет ✅

## 6. Структура + value test — PASS
- Хук → факты → split реплий → тезис (least privilege) → контраст (full vs scoped) → наш флот → honest gap → 3 практических пункта → вывод. Читается, есть takeaway для инженера (тест «revoke and check the owner notices nothing» — конкретный и запоминающийся).
- Value test: читатель уносит определение least privilege одной фразой + проверяемый тест ✅
- Длина: ~240 слов — в норме для X long-form.

## Итоговые фиксы (обязательные)
1. Добавить кредит: «…one sentence **@asifalis** left under my post…» — иначе FAIL по mentions.

Опциональные (не блокируют):
2. «Our fleet» → «My fleet» для консистентного first-person.
3. Можно добавить «per Axios» у факта о 5 банках (гигиена источников).
