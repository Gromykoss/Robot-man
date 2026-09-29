# LCM (hermes-lcm) — research pack для поста (собрано 21.09.2026)

## Триггер-пост
@witcheer, 20.09.2026 11:29 UTC, ID 2101634750473498915 — **28.7K imp / 500❤ / 34💬 / 647🔖 / 27 RT**.
Текст: «community member built a context engine plugin for long conversations: keeps every message in local SQLite, folds older turns into layered summaries, builds the live prompt from summaries + recent messages. Agent gets its own recall tools... plugs into the context engine slot Hermes exposes in config».
Автор: witcheer — community @NousResearch, ex @KPMG, 20.2K followers. Верифицирован API.

## Первоисточник: github.com/stephenschoettler/hermes-lcm
- **Lossless Context Management plugin for Hermes Agent** — DAG-based context engine, «never loses a message»
- **1.2k stars, 151 forks, 776 commits, 35 contributors**, язык Python (99.6%)
- Версия: **v1.0.0-rc.1** (релиз-кандидат, 04.09, PR #574: «tolerate transient SQLite sidecar churn»); последняя стабильная линейка v0.20.0 (24.07); 37 релизов
- Архитектура: engine.py (LCMEngine) + store.py (SQLite message store + FTS) + dag.py (summary DAG + FTS) + tools.py (lcm_grep, lcm_load_session, lcm_describe, lcm_expand, lcm_expand_query) + /lcm команды; 15 tools по manifest v1.0.0-rc.1
- Установка: git clone в ~/.hermes/plugins/hermes-lcm (или профиль) + config: plugins.enabled + context.engine: lcm
- Контракт ContextEngine ABC Hermes (developer-guide/context-engine-plugin.md): should_compress / compress(messages, focus_topic) / update_from_response — плагин встаёт в официальный слот движка контекста (Hermes v0.9+ custom ContextEngines)
- Смежное: issue NousResearch/hermes-agent #5701 «Pluggable context engines — enabling LCM as a plugin (like OpenClaw's lossless-claw)» — предложение о pluggable контекст-движках; origin — порт lossless-claw (OpenClaw) → lossless-hermes (r/hermesagent)
- GitHub contributor stephenschoettler = автор; X @SteveSchoettler (278 followers) — witcheer благодарил его «thanks for your contributions!» — вероятно тот же человек; ПЕРЕВЕРИТЬ при драфте (правило GitHub login ≠ X handle)

## Отзывы сообщества (тред + поиск, ~40 реплаев)
**Позитив:**
- @iamBarronRoth: «so good it should be default»
- @aiseomastery: «Never losing a message is huge»
- @NealFrazierTech: «recall tools are the interesting bit — layered summaries only stay honest if the agent can pull the original page back» (+ отдельный коммент Teknium: GitHub-first разумно, пока recall path движется)
- @AIAppsAPI: «keeping raw turns in SQLite alongside summaries is the right call — summaries are lossy in ways you cannot predict at write time»
- @RyanRayMartin: «layered summaries + exact recall tools is the right pattern for extended jobs»
- @Entropy_Badger, @jollyroger1480, @selfhosted4lyf («add this first thing»), @JamesOnEdge, @FazGPT — просят в plugin catalog/market
- @Teknium (cofounder Hermes Agent): вопрос «why this isn't on the plugins market yet :o» — сигнал, что команда заметила
- @sarlev_: «s/o @MartianEng / @jlehman_ / @rovnys / @SafePen on the lcm stuff» — атрибуция истоков LCM от сообщества (ПРОВЕРИТЬ, не утверждать в посте)

**Критика (для честных минусов):**
- @Raw_1975: «run hermes prompt-size A/B and you will see the size of lcm» — движок ест место в промпте
- @TankeryChan: SQLite растёт быстро, «hermes doctor recommends to prune this»
- @sorek_UK: «I been using it for a week and gotten used to "database corrupted" warnings» — реальные жалобы на коррапт БД (см. фикс «tolerate transient SQLite sidecar churn» в rc.1)
- @dreemd: «layered summaries plus recent turns is the shape i keep coming back to. but "lossless" is doing a lot of work in that na[me]» — сомнение в клейме lossless
- @yallgetscared: «Hermes keeps every session in a local SQLite store anyway, no? 😅» — вопрос отличия от стокового поведения
- @brsc2909 — шум/троллинг (jev-мем), игнор

## Наш dogfood (уникальный угол!)
**Мы сами работаем на Hermes-LCM прямо сейчас** — профиль robot-man крутится на этом движке контекста:
- Активные recall-инструменты в каждой сессии: lcm_grep (FTS5 по сырым сообщениям), lcm_recall (семантический поиск по всем сессиям), lcm_expand/lcm_load_session (дрill до сырых строк), lcm_recent (rollups по периодам)
- DAG-компакция: старые ходы сворачиваются в слои summaries, длинные сессии живут неделями
- Контрактный вопрос: recall policy требует exact evidence для цифр/SHA — «summary ≠ proof», сверка по исходникам. Это наш ежедневный опыт честности lossless
- Конкретные подтверждённые случаи сессии 21.09: востановление контекста после компакции, кросс-сессионный recall
- ⚠️ Уточнить у директора: наш движок = этот же плагин stephenschoettler или форк/интеграция? Формулировку dogfood согласовать с отчётом директора

## Метрики волны
Хайп-пост 28.7K imp, bookmark ratio 647/500 — выше лайков, практический контент. Ниша: Hermes-сообщество,Teknium в треде.

## Хендлы (верифицированы API 21.09)
- @witcheer — id 1452919031846117384, 20,223 followers, community @NousResearch ✅
- @SteveSchoettler — id 1989486553660608512 — СВЕРКА ПРОЙДЕНА 21.09: (1) @witcheer публично благодарит его за контрибьюции в треде; (2) независимый пост @trevin: «Hermes LCM by @SteveSchoettler» на @NousResearch instance. Два независимых подтверждения связи GitHub stephenschoettler ↔ X @SteveSchoettler ✅
- @Teknium — id 1365020011123773442 ✅
- @NousResearch — для mention при драфте
- Решение Сергея (TG 21.09): в посте упоминать @SteveSchoettler (после сверки — выполнена) и @witcheer

## Ждём от директора: отчёт собственного прогона/эксплуатации LCM

## Источники
- github.com/stephenschoettler/hermes-lcm; NousResearch/hermes-agent issue #5701 + docs context-engine-plugin.md
- Твит 2101634750473498915 + 40 реплаев треда (xurl, 21.09)
- r/hermesagent «Ported lossless-claw to lossless-hermes»
