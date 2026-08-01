# Reply Drafts — @gromykoss, 01.08.2026

**Стратегия (Grok Build, 01.08):** @gromykoss = primary channel сейчас. Реплаи > посты
(историч. avg 20.7❤️ на реплаях). «Daily substantive replies to HermesAgent builders».

**Правило:** ответы содержательные, с реальными цифрами/опытом. НЕ шаблоны (спам-фильтр).
Сергей постит вручную (через веб, т.к. API-реплаи только к mentions).
Каждый ответ ≤280 символов.

---

## 1. @rlaope — «Hermes memory system is something you're forced to build yourself» (2082685257715708029)

> Strong agree — and it's worth it. Ran mine at 98% memory and it started forgetting its own rules. Compressed to 44% with an audit, now memory is a first-class file I review weekly. Manual setup is the bottleneck, but that bottleneck taught me how the agent actually thinks.

**Почему работает:** конкретные цифры 98%→44% (реальный MEMORY audit), опыт-сторителлинг, не реклама.

---

## 2. @rlaope — «ONE and ONLY plugin required for hermes-agent — OMH» (2083147130051678286)

> Don't need a plugin for that — we rotate specialists instead. Grok Build owns X research, Codex owns code, Kimi does cheap inference, MoA (Grok + DeepSeek) verifies every output. The win wasn't a config flag; it was role assignment + a verify gate.

**Почему работает:** реальный метод делегирования (Diamond Pattern: Codex=код, Grok Build=X, Kimi=inference, MoA=verify), без Claude (мы его не используем), лёгкий пушбэк «плагин не нужен» — не просто согласие.

---

## 3. @DamiDefi — «What happens after you build 10 agents» (2082836368410218692)

> 10 agents = 10 outputs you have to trust. We solved it with a verify gate: nothing ships unless a second pass (different model) checks it. The bottleneck moved from "writing" to "verifying" — and that's the honest part nobody shows.

**Почему работает:** отвечает на главный тезис (агенты создают больше работы), даёт наш механизм (MoA/verify gate, разная модель), честный вывод.

---

## 4. @beamnxw — «Harness engineering paper — ETCLOVG» (2082746025958150333)

> We found the same thing the hard way: the model never changed, but our harness did — sandboxing, context layering, verifiers — and reliability went up. The model is 20% of the system; the other 80% is how you run it.

**Почему работает:** соглашается + усиливает личным опытом (context-layering, verification-loop), конкретная пропорция как запоминающийся хук.

---

## Статус
- [ ] 01.08: 4 драфта готовы. Показать Сергею → апрув → ручной постинг через веб.
- [ ] Не постить через API (не mentions, X блокирует).
- [ ] Лимит: 1-2 реплая/день (частота >2/день = пессимизация).
