# PROJECT_MEMORY_GRAPH.md — единый вход сессии robot-man

> Назначение: компактная карта проекта, читается на старте вместо больших доков.
> Обновляется: при изменении доменов / инвариантов / контрактов (Spec Drift Gate, внизу).

## Purpose
Robot-man — исполнитель X/Twitter-контент-фабрики для @RobotsTJ500 и @gromykoss: берёт бриф Hermes, пишет в каноне голоса, готовит обложку/MoA/факт-чек и публикует только после Human Gate.

## Boot Rule
1. На старте читай только этот граф + Gates из `AGENTS.md`; остальные доки открывай по маршруту из Change Routing.
2. Задача про домен → открой строку домена в Domain Map, затем только указанные источники.
3. `context_loader.py` остаётся обязательным (rule 0): «не читать целиком» ≠ «не запускать loader». `CHRONOLOGY.md` — только последние 3 дня / через loader, не весь файл.

## Global Invariants (нарушение = стоп + эскалация)
- **Язык:** все мысли, ответы и обсуждения — только на русском, без исключений. EN только как финальный текст поста @RobotsTJ500 после RU-approval.
- **Human Gate:** никогда не постить без явного approval Сергея: «ок» / «пости».
- **Публикация:** только `post_with_log.sh` + обложка; прямой `xurl post` запрещён. Text-only только с явным `ALLOW_TEXT_ONLY=1`.
- **Delivery Package Gate:** RU-драфт + файл, EN-финал после ok, `MEDIA:/abs/path`, joint MoA, факт-чек/MoA summary.
- **Голос:** `VOICE_PROFILE.md` + `ENGINEERING_POST_TEMPLATE.md` — канон @RobotsTJ500; `VOICE_PROFILE_GROMYKOSS.md` — канон @gromykoss. ALL-CAPS/реклама/попса запрещены.
- **Факты:** цифры, даты, имена только из `CONTENT_BRIEF.md` или `CHRONOLOGY.md`; нет в источнике → факта нет.
- **API limits:** max 3 public writes/day, follow max 2/day (hard 3), 429 → STOP.
- **Security:** OAuth/xurl credentials не логировать, не коммитить, не показывать.

## Domain Map

| Домен | Источники правды | Код / артефакты | Риски |
|-------|------------------|-----------------|-------|
| content-briefs | `CONTENT_BRIEF.md`, `CONTENT_BRIEF_STANDARD.md`, `CONTENT_BRIEF_TEMPLATE.md`, `briefings/` | `drafts/`, `DRAFT_BANK_RTJ.md` | выдуманные факты, EN-first |
| voice | `VOICE_PROFILE.md`, `ENGINEERING_POST_TEMPLATE.md`, `VOICE_PROFILE_GROMYKOSS.md` | `data/voice_updates/`, `lessons.md` | рекламный тон, ALL-CAPS, hashtags |
| strategy | `STRATEGY.md`, `CONTENT_STRATEGY.md`, `TACTICS*.md`, `STORY_ARC.md` | — | robot-man решает стратегию вместо Hermes |
| x-infra | `AGENTS.md`, `post_with_log.sh`, `published_posts.jsonl`, `data/write_counter.json` | `operators/operator_limits.py`, `operators/operator_approval.py`, `scripts/offpipeline_watchdog.py`, `data/write_counter.json`, `data/engagement_log.jsonl` | прямой post, лимиты, credentials |
| knowledge-graph | `CIRCULATION_GRAPH.md`, `knowledge_graph/graph.json` | `knowledge_graph/{query_tool,maintenance,schema}.py`, `scripts/knowledge_graph.py` | анализ без KG, drift edges |
| analytics | `reports/`, `data/metrics/`, `scripts/analytics_loop.py` | `scripts/analytics_loop.py` | неверный baseline, stale metrics |
| shadowban-recovery | `SHADOWBAN_RECOVERY.md`, `BUGS.md`, `CHRONOLOGY.md` | `scripts/offpipeline_watchdog.py` | шаблонные replies, off-pipeline writes |
| tailcat-war-story | `research/tailcat-research-20260901.md`, `CONTENT_BRIEF_tailcat_20260901.md`, `CHRONOLOGY.md` | `drafts/tailcat_*`, `images/tailcat_*` | повтор темы, неподтверждённые claims |
| session-handoff | `SESSION_STATE.md`, `CHRONOLOGY.md` (последние 3 записи) | approval/token state, current drafts | продолжение старого состояния как текущего |

## Change Routing (задача про X → читать Y)
- **Новый пост / delivery package** → content-briefs + voice + knowledge-graph + x-infra.
- **Правка голоса / правки Сергея** → voice + `sergey-edit-absorb` при необходимости.
- **Публикация / reply / follow / API write** → x-infra + shadowban-recovery + лимиты из `AGENTS.md`.
- **Аналитика / nightly / охваты** → analytics + knowledge-graph + последние 3 записи `CHRONOLOGY.md`.
- **Дубли тем / ручные посты @gromykoss** → content-briefs + `published_posts.jsonl` + `operators/published_topic_check.py`.
- **Обложка / media** → voice + drafts/images по теме + joint MoA.
- **Tailcat / OpenSpec continuation** → tailcat-war-story + content-briefs + chronology.
- **Баг / guard / watchdog** → shadowban-recovery + x-infra + `BUGS.md`.
- **Стратегия / TACTICS / STORY_ARC** → strategy (только чтение; решения — зона Hermes).
- **Продолжить сессию / handoff / approval.token** → session-handoff + `SESSION_STATE.md` + последние 3 записи `CHRONOLOGY.md`.

## Spec Drift Gate
Изменил домен / инвариант / контракт маршрутизации → обнови этот граф + `CHRONOLOGY.md`. Если изменение не затрагивает контрактный индекс — запиши в `CHRONOLOGY.md`: `Contract index update: not needed`.
