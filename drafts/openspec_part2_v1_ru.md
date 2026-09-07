# openspec_part2_v1_ru
# @RobotsTJ500 · продолжение 2096102362003751175 · War Story part 2
# Факты только из CONTENT_BRIEF 05.09 (часть 2). Hashtags: 0 (канон 05.09).
# Обложка: drafts/covers/openspec_part2_v1_cover.png
# Human Gate — без «пости» не публиковать.

---

## Текст (RU)

Утром собрали contract index для construction-site WhatsApp-бота.
К вечеру индекс уже не «схема на бумаге» — он ловил дрейф и показывал рост.

Граф. knowledge_graph/graph.json: **397 узлов / 610 рёбер**
(на 16.08 было 316/515; пересборка каждые 6ч).
Для Obsidian: **126** заметок с [[вики-связями]] + canvas **126** узлов / **141** ребро.
Цифры растут, потому что индекс читают, а не потому что «нарисовали красиво».

Дрейф в бою. В текстах ещё жило «14 таблиц ОЖР».
Канон графа — **15**.
Закрыли в **9** местах: README ×6, PROJECT ×2, AGENTS ×1
(коммиты `363fd9d`, `ae8fb06`).
Не интуиция. Сверка с git и с графом.

Gate. В AGENTS.md — **CONTRACT INDEX GATE**:
глубокие доки только через доменную карточку;
после правки домена — обнови граф/карточку **или** явно напиши
`index update: not needed`
(`ae62186`).

Петля хроники. Guard в `.git/hooks/post-commit`:
коммиты `chrono:` больше не пишутся в CHRONOLOGY.
Проверочный `4bf4767` в журнал не попал — как и задумано.

Закрытие программы. Merge `d200ad4` (--no-ff).
pytest: 23 smoke + полный прогон 124 (03.09) — зелёный.
health: :3000 connected, :8099 ok.
В корне entry — ровно **16** .md; точка входа — PROJECT_MEMORY_GRAPH.md.

Урок части 2 (без пересказа части 1):
контракт — живой контур.
Если правила держат — метрики ползут вверх, а устаревшая цифра
не прячется в README до следующего инцидента.

Building in public. 🤖

---

## Fact check map (EN will use same digits)

| digit | brief # |
|-------|---------|
| 397 / 610 | 2 |
| 316 / 515 | 2 |
| 126 / 126 / 141 | 2 |
| 14 → 15, 9 places | 3 |
| CONTRACT INDEX GATE, ae62186 | 4 |
| d200ad4, 23 smoke, 124, :3000/:8099 | 5 |
| chrono guard, 4bf4767 | 6 |
| 16 root .md | 7 |

Hashtags: **none** (override brief legacy row; Sergey 05.09).
Self-reply: no. URL in body: no.
