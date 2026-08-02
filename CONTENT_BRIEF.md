# CONTENT_BRIEF — 2026-08-02

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @gromykoss

---

## Тема

Shadowban @RobotsTJ500 длился 16 дней. Причина найдена: AI-агент нарушил правила автоматизации X с первого дня — не поставил метку «automated». Не «злой алгоритм» — мы сами.

## Факты (верифицированы Hermes)

| # | Факт | Источник |
|---|------|----------|
| 1 | @RobotsTJ500 в search shadowban 16 дней (с 17.07). `from:RobotsTJ500` → 0 результатов. Прямые ссылки работают (200 OK) | robot-man CHRONOLOGY — 01.08 23:06 |
| 2 | Корень найден 01.08 00:14: X Automation Rules (апрель 2026) требуют метку «automated» и связь с human-run аккаунтом для ВСЕХ аккаунтов использующих API. @RobotsTJ500 нарушил с первого дня | hermes-vault `f9516a5` Root cause: automated account label missing |
| 3 | Официальная цитата: «X may take action on your account, including **filtering your posts from search results**» — это точное описание нашего shadowban | help.x.com/en/rules-and-policies/twitter-automation.html |
| 4 | Фикс: Settings → Automation → выбрать @gromykoss как управляющий аккаунт + включить метку «Automated». Делается только вручную — API для этого нет | hermes-vault research |
| 5 | Другие нарушения: отсутствовал mandatory bio disclosure (требование: «automated by @gromykoss» или «bot by @gromykoss») | Тот же источник |

## Контекст проекта

**Проект:** robot-man + Hermes-vault (оператор)
**CHRONOLOGY:** `/home/hermes-workspace/robot-man/CHRONOLOGY.md` (раздел 2026-08-01)
**AGENTS.md:** `/home/hermes-workspace/robot-man/AGENTS.md`
**Hermes-vault research:**
- `~hermes-vault/40_Research/Articles/shadowban-x-research-2026-07-31.md` (99 строк)
- `~hermes-vault/40_Research/Articles/shadowban-root-cause-automated-label-2026-07-31.md` (48 строк)

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story — личный опыт |
| Аккаунт | @gromykoss |
| Голос | Русский, тёплый, ироничный — «дневник киборга» |
| Длина | до 280 символов (или 4000 если тред — решать robot-man) |
| Hashtags | #Shadowban #AIAgents #HermesAgent #BuildingInPublic |
| Изображение | нет |

## Запрещено

- Обвинять X / «злой алгоритм» — мы НАРУШИЛИ правила, это не жертва
- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда)
- Технический жаргон без пояснения — аудитория @gromykoss шире чем @RobotsTJ500

## Tone-направление

«16 дней мы думали что X нас душит. А оказалось — наш AI-агент с первого дня нарушал правила. Сами себя забанили.» — ирония, самоирония, урок для всех кто запускает AI-агентов в соцсетях.

## Deadline

**Черновик к:** 10:00 UTC 02.08
**Публикация:** после approval Сергея (ручной постинг @gromykoss)

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md robot-man (раздел 01.08)
3. Прочитать AGENTS.md robot-man (контекст)
4. Написать драфт в голосе @gromykoss (VOICE_PROFILE_GROMYKOSS.md) — русский, тёплый, ироничный
5. MoA-проверка: `/moa deepseek-xai` + `/moa viral-score`
6. Факт-чек: сверить каждую цифру с брифингом
7. При нарушениях → переписать
8. Отправить драфт на approval Сергею
9. После «ок» → ручной постинг Сергеем
