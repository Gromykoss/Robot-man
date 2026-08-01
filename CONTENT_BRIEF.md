# CONTENT_BRIEF — 2026-08-01

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## Тема

I audited my own git history and found my secrets. The AI agent that committed its own credentials — and had to surgically remove them from 63 commits.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | CRITICAL: Matrix Access Token найден в `gulag-inject.js` (строка 502) — скомпрометирован | robot-man/CHRONOLOGY.md — 2026-07-31, аудит безопасности |
| 2 | HIGH: пароль GULAG `Gromykoss1306!` найден в 5 тестовых файлах (test_login.py, test_member_popup.py ×3, test-member-popup.mjs) | robot-man/CHRONOLOGY.md — 2026-07-31 |
| 3 | CRITICAL: X cookies (`auth_token` + `ct0`) найдены в `x-monitor.deprecated/.env` (не в git, только на диске) | robot-man/CHRONOLOGY.md — 2026-07-31 |
| 4 | `git filter-branch --tree-filter` очистил все 6 файлов из 63 коммитов (ветки main + main.war_story_draft) | robot-man/CHRONOLOGY.md — 2026-07-31 |
| 5 | Ветка `main.war_story_draft` удалена. `git reflog expire` + `git gc --aggressive --prune=now` — полная очистка | robot-man/CHRONOLOGY.md — 2026-07-31 |
| 6 | Двойной аудит безопасности профиля Robot-man — инициатор: плановый security sweep | robot-man/CHRONOLOGY.md — 2026-07-31 |

## Контекст проекта

**Проект:** robot-man
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» |
| Длина | до 4000 (note_tweet) |
| Hashtags | #BuildingInPublic #AIAgents #SecurityAudit |
| Изображение | да — security audit visual (темница/фонарик/красный код) |

## Запрещено

- НЕ называть пароль `Gromykoss1306!` в тексте поста (security)
- НЕ показывать фрагменты токенов
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)

## Tone-направление

Спокойный, самоироничный: «я — AI-агент, который накоммитил секреты в свой же репозиторий, а потом сам себя отаудировал». Без паники, без «мы всё исправили». Просто: вот что случилось, вот как чинили, вот урок.

## Deadline

**Черновик к:** 10:00 UTC 01.08.2026 (Daily Content Gate)
**Публикация:** после approval Сергея

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md указанного проекта (раздел за последние 3 дня)
3. Прочитать AGENTS.md указанного проекта (контекст)
4. Написать драфт в голосе аккаунта (см. VOICE_PROFILE.md / VOICE_PROFILE_GROMYKOSS.md)
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → `bash post_with_log.sh "текст"`
