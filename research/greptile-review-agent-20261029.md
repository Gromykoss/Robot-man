# Research pack — Greptile «How to Build an AI Code Review Agent» (IDEA-7) — 29.10

## Первоисточник
- **YouTube: Daksh Gupta (co-founder Greptile), AI Engineer, 26.10.2026** — https://youtu.be/4UtrRVtUN_g (18:26, 37K views)
- Контекст Greptile: ревьюят ~1% всех PR на GitHub

## Ключевые факты доклада
- Простая версия (sandbox + agent + webhook) не ловит баги, стоит $3-25/PR и заливает nitpick'ами
- **Fix 1:** targeted prompts, меньше nitpicks (определение nitpick: «технически верно, но педантично»)
- **Fix 2:** датасет исторических PR-инцидентов
- **Fix 3:** model inversion — ревью Claude-кода через GPT и наоборот ловит **~10% больше багов**
- **Fix 4:** codebase context + living wiki (docs, tickets)
- **Fix 5:** autonomous testing в sandbox с computer use
- **Fix 6:** дешёвые модели на большинство подзадач

## Связь с нашим мандатом (владелец → директор, 29.10 02:45)
Мандат «Апгрейд ревьюера — 4 этапа» построен на этом докладе (gap-анализ reviewer-gap.md):
- Fix 2 → Этап 1 (eval review-catch, датасет из ≥10 реальных дефектов вердиктов)
- Fix 3 → Этап 2 (model inversion, maker{family}, триаж L2-L3 другой кит)
- Этап 3 (лимит 3 re-gate, эскалация) — наш, из практики
- Fix 4 → Этап 4 (каталог типов багов из 128 вердиктов, never same feedback twice)
- Правило владельца: цифры Greptile (+10%) НЕ переносить — «мерить своё»

## Наша фактура (уже опубликовано, дуги 24-27.10)
- Maker ≠ Checker доказан живьём: grok-checker поймал 2 ложнозелёных пути в моём скорере (пост 24.10 gate-on-gates)
- Model inversion = наш MoA-процесс (рецензенты независимо, право не соглашаться)
- dair_ai (Competitor Watch 28.10): критик рядом с главным = +5.9-9.5 п. при 1.13-1.25× латентности
- «review ok = not found, not_run обязателен» — тезис gate-on-gates
- Honest минусы: write-path не формализован («a patch until it is a pipeline»)

## Ограничения поста
- ⛔ Мандат/апгрейд в пост НЕ входит до реализации (гейт факт-не-обещание); пост = разбор доклада + наша независимая практика
- DUP: enforced canon 25.10 (5 дней) — угол другой («кто проверяет проверяющего» vs «rules vs code»), ручная сверка обязательна
- Хендлы: @greptile (продукт-герой доклада — mention обязателен), @dakshgupta? (верифицировать спикера), @dair_ai (по релевантности)

## Статус
- IDEA-7, кандидат поста ПОСЛЕ реализации мандата (RECEIPT директора: baseline/catch rate цифры — тогда добавляются наши)
- Угол: «What a 2026 talk gets right about review agents — and what our fleet already proved»
