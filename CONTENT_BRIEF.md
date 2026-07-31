# CONTENT_BRIEF — 31.07.2026

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** два поста для @gromykoss — обновление статуса проектов

---

## ПОСТ 1 — GULAG.online: 9 дней после «5 агентов»

### Тема

Что изменилось в GULAG.online за 9 дней после поста про 5 Hermes-агентов.

### Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | 11 активных пользователей | GULAG CHRONOLOGY.md, Matrix API |
| 2 | v109 APK: исправлен баг клавиатуры (зазор + тулбар), 2 круга Codex+Grok → 100% PASS | GULAG CHRONOLOGY.md 27.07.2026 |
| 3 | Ketesa v1.4.0 на /admin/ — Basic auth + fail2ban | GULAG CHRONOLOGY.md 28.07.2026 |
| 4 | Diamond Pattern Pilot #2: bug-fix/deploy/audit workflows | GULAG AGENTS.md |
| 5 | Kimi K3: 1M контекст, $3/M input | GULAG CHRONOLOGY.md 24.07.2026 |
| 6 | Codex + Grok Build — весь код, нулевая маржинальная стоимость | GULAG AGENTS.md (CNC-ПРАВИЛО) |
| 7 | Само-хост: Matrix/Synapse, Vanilla JS клиент, Expo app, Ketesa | GULAG AGENTS.md |
| 8 | nginx Basic auth конфликт с Synapse — решён через map по Authorization | GULAG CHRONOLOGY.md 28.07.2026 |
| 9 | Кастомные эмодзи «СИМВОЛЫ ЗОНЫ» (28 символов) | GULAG CHRONOLOGY.md 05.07.2026 |

### Контекст проекта

**Проект:** GULAG
**CHRONOLOGY:** `/home/hermes-workspace/gooolag/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/gooolag/AGENTS.md`

### Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | Tech Breakdown — thread (2-3 твита) |
| Аккаунт | @gromykoss |
| Голос | Русский, производственный, без хайпа |
| Длина | до 280 × 3 |
| Hashtags | #BuildInPublic #Hermes #Matrix #SelfHosted #AI |
| Изображение | нет |

### Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Упоминать GitHub-репозиторий (приватный)

### Tone-направление

Сухо, по делу, с гордостью за production-результат. «Вот что мы построили за 9 дней.»

### Ссылка на старый пост

https://x.com/Gromykoss/status/2079392228754284866 — «5 Hermes agents, 1 senior, 4 juniors, GULAG — prison warden»

### Deadline

**Черновик к:** 18:00 UTC
**Публикация:** после approval Сергея

---

## ПОСТ 2 — Robot-man: обновление статуса

### Тема

Что изменилось в robot-man после поста про Knowledge Graph (117 nodes).

### Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | Knowledge Graph: cron каждые 6 часов перестраивает граф | robot-man AGENTS.md |
| 2 | Diamond Pattern: Split → 3 research streams → Merge → MoA Check → Human Gate | robot-man AGENTS.md |
| 3 | Content pipeline: Hermes (BRIEF) → robot-man → MoA → approval → публикация | robot-man AGENTS.md |
| 4 | Два аккаунта: @RobotsTJ500 (AI-агентность, техника), @gromykoss (личный бренд, производство) | robot-man AGENTS.md |

### Контекст проекта

**Проект:** robot-man
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`

### Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | Simple Insight — 1 твит |
| Аккаунт | @gromykoss |
| Голос | Русский, сжато, обновление статуса |
| Длина | до 280 |
| Hashtags | #BuildInPublic #Hermes #KnowledgeGraph #AI |
| Изображение | нет |

### Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)

### Tone-направление

Короткое обновление: граф жив, пайплайн работает, два аккаунта.

### Ссылка на старый пост

https://x.com/Gromykoss/status/2080590958547100042 — «knowledge graph 117 nodes, 109 edges, kimi k3 primary model»

### Deadline

**Черновик к:** 18:00 UTC
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md указанного проекта (раздел за последние 3 дня)
3. Прочитать AGENTS.md указанного проекта (контекст)
4. Написать драфт в голосе аккаунта (см. VOICE_PROFILE_GROMYKOSS.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
