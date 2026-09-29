# Jev (TypeSafe AI) — research pack для поста (собрано 20.09.2026)

## Что это (первоисточник: typesafe.ai, blog 15.09.2026, docs.typesafe.ai)
- **Jev** = первый публичный «System One model» TypeSafe AI. НЕ генерирует текст: принимает unstructured state + типизированные вопросы → возвращает типизированные решения с калиброванными вероятностями, один параллельный проход.
- Архитектура: новый sampler (не autoregressive) + обучение **RLCD** (Reinforcement Learning for Calibrated Decisions) — позиционируется против RLHF/RLVR.
- Основатель: **Diogo Almeida** — по DataCamp, соавтор ChatGPT в OpenAI.
- Заявленные цифры (сам сайт TypeSafe): **193.6x faster, 444.6x cheaper** (по их workflow-бенчмаркам); $0.042/1M input токенов ($42/млрд), output бесплатный; latency 70–500ms; demo: решение за 0.114s за $0.000081; rate limits 250K tok/s, 1200 req/min; лимит запроса 64k токенов; модель jev-1.13.0.
- Клейм «0% structured output error / 0% tool call error» — «невозможно по построению» (схема ограничивает вывод). Сравнение TypeSafe: у GPT luna/terra 0.58% ошибок structured output, Opus 5 — 5.73%, Haiku 4.5 — 45.5%; tool calls: GPT-5.6 Sol 17%.
- На 4-workflow бенчмарке TypeSafe: ~68% accuracy, «близко к mid-tier LLM», но дешевле в 40–400x и быстрее в 20–200x (DigitalCamp summary).
- Ограничения (сами docs): плох на контексте, нерелевантном вопросу; max 255 опций в вопросе (253 кандидата); нет объяснения «почему» — только число.

## Use case «instant compaction» (тема хайп-волны)
- Хайп-твит (17.09, ID 2100694549362553153): «perfect use case for @typesafeai Jev: instant compaction — в 2026 почему компакция всё ещё summarization-промпт? Jev может скорить каждый tool call и дропать нерелевантное» — **3.7M показов, 10.7K лайков**.
- Механика реальных обёрток (explainx fast-jev-compaction, LiteLLM guardrail):
  - Парные tool_use/tool_result; первые N сообщений (default 6) закреплены.
  - Jev отвечает на 2 yes/no вопроса на вызов: держать ли сам вызов, держать ли результат дословно. Порог keepThreshold ~0.5 (LiteLLM: relevance_threshold 0.2).
  - Всё-or-nothing на exchange: держится дословно или заменяется notice'ом; суммаризации нет.
  - LiteLLM: переписывается только input запроса; guardrail down → трафик идёт без компакции.

## Контраргументы (столб «confirmed/rejected» будущего поста)
### Teknium (19.09, tweet 2101398453578555898; 140K imp) — reproducible eval
- Прогнал на публичном compaction eval (github.com/NousResearch/hermes-agent, PR #116246): результат эквивалентен правилу «удалить все tool calls из истории» — никакая модель не нужна.
- Порочный круг: с каждой компакцией tool calls всё меньше → сжимается всё меньше → hard stop.
- Каждая компакция ломает кэш → 10x цена input; выше baseline после компакции.
### Theo (@theo, tweet 2100762304862384257; 629K imp, 2.5K лайков)
1. Компакция ≠ фильтр; должна использоваться редко, не постоянно.
2. Jev в этой реализации не видит ни истории решения, ни результата tool call → риск «stupid loops».
3. Reasoning traces у frontier-API шифрованы — Jev их не видит и дропает (Anthropic требует полную историю для reasoning) → модель тупеет.
4. Frontier-модели уже обучены на своих компакционных флоу.
5. Cache writes дороже reads; правка истории инвалидирует кэш до конца: удалить «2» из «1..6» = переписать «3..6» — дороже, чем оставить. (Theo: cache writes >60% его LLM spend.)
### Anthony Maio (Substack): «can't hallucinate» требует оговорки — валидный ответ ≠ правильный; воркфлоу-бенчмарки создавал сам TypeSafe (признанный design bias).
### tonysimons_ (20.09, 7.4K imp): общий тезис «benchmarks before adoption».

## Метрики волны
- Хайп: 3.7M imp. Theo: 629K. Teknium: 140K. Tony: 7.4K. Запросов ветки: compaction-дискурс ценнее самого Jev-хайпа.

## Верифицированные хендлы (API, 20.09)
- @typesafeai — id 2014504062797152256, verified business, 115,428 followers. ✅
- @Teknium — id 1365020011123773442, cofounder/lead engineer Hermes Agent @NousResearch. ✅
- @tonysimons_ — id 1998221941300490241. ✅
- @theo — автор поста 2100762304862384257 (id из includes: 1365020011123773442 — НЕТ, это Teknium; у Theo отдельный id, взять из t4.json при драфте).
- ⚠️ @theo при драфте верифицировать отдельно /2/users/by/username.

## Открытые позиции для поста
- Собственный прогон компакции на Hermes Agent — сделает директор, отчёт ждём (вставить в confirmed/rejected).
- Честность: Jev как идея (typed decisions, calibration, дешёвый System-1 слой) ≠ конкретная compaction-обёртка. Судим обёртку, не идею.

## Источники
- typesafe.ai (home, blog introducing-system-one-models-and-jev), docs.typesafe.ai
- docs.litellm.ai/docs/proxy/guardrails/typesafe
- explainx.ai fast-jev-compaction; pydantic.dev/docs/ai/models/typesafe
- DataCamp system-one-models-jev; marktechpost 19.09; anthonymaio.substack.com
- Твиты: 2100694549362553153 (хайп), 2101398453578555898 (Teknium), 2100762304862384257 (Theo), 2101497851209457932 (Tony)
