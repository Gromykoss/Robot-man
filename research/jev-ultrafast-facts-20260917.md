# Jev Ultrafast (Browser Use) — факт-база (собрана 17.09, пост планируем через ~2 дня)

**Статус:** отложено Сергеем 17.09 — «это то же, о чём наш прошлый пост» (chrome-agent 16.09 + BrowserSkill 17.09 = два browser-поста подряд; третий сразу — дубль темы). Постить через пару дней.
**Триггер:** пост @tonysimons_ 2100656340817633313 (18:41 UTC 17.09, 6.4k imp / 99❤ / 131🔖 за 5ч).
**Угол при постинге:** скорость цикла browser-агента — не доступ (BrowserSkill), не верификация (chrome-agent), а стоимость решений. Дуга «browser loop rebuilt piece by piece».

## Что это

browser-use/jev-ultrafast, MIT, © 2026 Browser Use. Python, всего 743 строки. Динамическое индексированное action space: page → element table → **один** TypeSafe-запрос выбирает операцию + target (speculative target heads — исполняется только выбранной операции). TYPE_TEXT зовёт маленькую LLM (Mercury) только для генерации текста. Операции: CLICK, TYPE_TEXT, SELECT, SCROLL_UP/DOWN, WAIT, DONE, BLOCKED. Никаких селекторов или кода от модели.

## Верифицированные цифры (клон /tmp/jev, docs/performance.md)

| # | Факт | Источник |
|---|------|----------|
| 1 | Google Flights Zürich→London: 7.073 s @1×, полный путь включая загрузку результатов | docs/performance.md |
| 2 | Matched comparison 3 пары прогонов: медиана 9.450 s → 7.092 s (−25.0%), Jev-запросы 22→17, browser protocol calls 1092→101 | docs/performance.md |
| 3 | Их собственная оговорка: «three pairs are too few for a strong statistical claim (sign-test p = 0.25), not a broad agent benchmark» | там же |
| 4 | Медиана латентности Jev-запроса 178 ms; запись: 17 Jev requests, 10 интеракций + 1 WAIT, 2 helper-колла | там же |
| 5 | Текст генерируется настоящей LLM: Zurich 581 ms, London 346 ms; OpenRouter $0.00006272 за 2 текст-колла (только helper, не total cost) | там же |
| 6 | 90,558 input / 6,325 output TypeSafe токенов на записанный прогон | там же |
| 7 | Другие чеки: Wikipedia (Gödel) 2.798 s — точный URL статьи; hotel fixture 1.896 s — property + 3 фильтра | там же |
| 8 | Почему быстрее: старый цикл инвалидовал решения на каждом DOM-мутации (включая анимации) и перечитывал a11y-дерево + резолвил сотни DOM-нод; новый снапшот читает common HTML/ARIA-контролы одним browser-вызовом | там же |
| 9 | Замеры в JSON (flights-measurement.json, full-speed-measurement.json), верификация независимая, демо @1× без ускорения | репо |
| 10 | AGENTS.md культура: «A DONE choice is not proof of success», «Never retry a browser mutation», «Verify actual final outcomes independently» | AGENTS.md клона |
| 11 | Зависимость: нужен TypeSafe API key (docs.typesafe.ai) + TEXT_MODEL_API_KEY; репо полностью открыт, waitlist-замечание @voipjedi в треде — про TypeSafe API, не про репо | README + тред |
| 12 | Пост Тони: 6,418 imp / 99❤ / 131🔖 / 8💬 за ~5ч (live 23:5x UTC 17.09) | xurl live |

## Что НЕ хвалить

- p = 0.25 — их собственный статистик честно говорит «weak claim»; не подавать 1092→101 как доказанный benchmark
- TypeSafe (Jev) — проприетарная модель-зависимость: «open source» репо, но ядро-полиси у стороннего API. Смешанный open/closed
- 3 пары прогонов, одна задача (Flights) — n крошечный
- $0.00006272 — только текст-хелпер, полная стоимость задачи не раскрыта

## Mentions (верифицировать перед драфтом)

- @tonysimons_ — верифицирован live (id 1998221941300490241, 11,472 followers) ✓
- @browseruse — проверить /2/users/by/username ПЕРЕД драфтом
- Reply в тред Тони ЗАБЛОКИРОВАН (403-политика: он нас не упоминал)

## Связь с нашей дугой

chrome-agent 16.09 (верификация каждого действия) → BrowserSkill 17.09 (доступ к настоящему браузеру) → Jev (стоимость/скорость решений). Три части одного пересборки browser-цикла. В посте: 1 строка связки с нашими двумя постами, остальное — Jev.

## ДОПОЛНЕНИЕ 17.09 (Сергей): Browserbase — кандидат во второй пост через пару дней

**Решение Сергея:** и Jev, и Browserbase — кандидаты в посты через пару дней (после browser-паузы). Возможна карта-пост: Jev (скорость) + Browserbase (облако) + BrowserSkill (локальный залогиненный Chrome) = три модели browser-инфраструктуры для агентов.

**@browserbase — верифицирован live 17.09:**
- Verified, 21,344 followers, bio: «give your agents access to the whole web - creators of @stagehanddev»
- Продукт: облачные headless-браузеры для агентов (контраст с BrowserSkill = локальный браузер)
- Недавние посты: Muse Code plugin, browse CLI (docs.browserbase.com/integrations/skills/browse-cli), n8n интеграция, one-click deploy templates
- Посты маркетинговые/анонсовые, без инженерной глубины — для поста брать первоисточники (docs, stagehand repo), не их ленту

**@browser_use — верифицирован live 17.09:** id 1861811243813666816, 47,127 followers, «Agents that use the Browser», 1939 твитов. Handle browseruse — SUSPENDED (учитывать при mention: только browser_use).
