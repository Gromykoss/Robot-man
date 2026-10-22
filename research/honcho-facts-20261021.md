# Fact-base: Honcho (тема 3, депозит Hermes 21.10 — первоисточники проверены директором)

## Вердикт директора (для поста)
- Honcho — доп. слой рядом с decisions.md; **md остаётся каноном аудита**
- Пилот self-host на VPS, гейт 2-4 недели: **honcho_search должен бить grep по decisions.md, иначе выводим**
- Решение о пилоте — за владельцем

## Продукт [GitHub API + honcho.dev, проверено 21.10]
- Открытый memory-сервер для stateful-агентов; AGPL-3.0; **7.7k★**; push 21.10; релиз v3.3.0 (14.10)
- Self-host: docker-стек api + deriver + mcp + postgres(pgvector) + redis, порты 127.0.0.1
- Гибридный retrieval (keyword + vector) + dialectic-чат
- **Dreamer** периодически удаляет устаревшие conclusions (консервативный подход vs наш append-only)

## Прайсинг облака [их блог honcho-3, их заявления]
- Инжест $2/1M токенов; storage и retrieval бесплатны
- context(): бесплатный, безлимитный, ~200ms, на каждый ход
- chat(): minimal $0.001 / low $0.01 / medium $0.05 / high $0.10 / max $0.50 за запрос
- dreaming бесплатен
- Self-host: тарифы не применяются, платишь только токены своего провайдера
- Честная деталь: прайсинг-страницы нет (honcho.dev/pricing → 404); quickstart пишет $5+$5/мес, ToS — one-time credit — формулировки расходятся

## Схема [docs v3 architecture]
- Workspace (топ-изоляция, auth, конфиг) → Peers + Sessions; Peer many-to-many Sessions
- Session хранит Messages (JSONB metadata); каждый message триггерит фоновый reasoning
- Peer = любая сущность (юзер/агент), unified paradigm; cross-session: выводы о peer из одной сессии информируют другие
- Session = тред с временными границами; single-peer session = импорт внешних данных (emails/файлы как messages); scopes ограничивают recall
- Нюанс v3: summaries и peer cards переезжают в Dreaming — доступны не сразу, доки: «не полагаться на них в вакууме»

## Сравнение с mem0 [GitHub API, не их README]
- mem0ai/mem0 — **67575★**, Apache-2.0, push 21.10, Python; mem0-mcp 662★; openmemory 99★ MIT
- mem0 OSS = библиотека/SDK: vector-обвязку поднимаешь сам, peer-представлений из коробки нет; их Platform = SaaS
- Honcho = самодостаточный сервер (AGPL): peer-представления + dialectic-агент + self-host из коробки
- Их benchmark-заявления (Pareto dominant, 5x cost reduction) — их marketing; наш вердикт опирается на свой гейт, не на их цифры

## Ось поста (тема 3)
«Consolidation vs append-only» + пилот-гейт. Их pass удаляет заменённое — против append-only Decisions.md (stale+pointer). Вывод директора: Honcho доп. слоем, md = канон аудита. Публикация — после решения владельца о пилоте.
