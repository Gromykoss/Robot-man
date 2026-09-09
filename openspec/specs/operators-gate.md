# operators-gate

## Domain
operators-gate

## Purpose
Операторские гейты robot-man для X/Twitter-пайплайна: enum-контракт verdict, финальный checklist перед публикацией, allow-list аккаунтов, approval/write-counter контур, дедуп тем и loop guard. Карточка фиксирует только ассертимую семантику из `operators/tests/test_operators.py`; сеть, `xurl` и реальные публикации не входят в unit-контур.

## Files
- `operators/verdict.py`
- `operators/operator_checklist.py`
- `operators/operator_account.py`
- `operators/operator_pipeline.py`
- `operators/operator_approval.py`
- `operators/operator_factcheck.py`
- `operators/operator_limits.py`
- `operators/published_topic_check.py`
- `loop_guard.py`
- `operators/tests/test_operators.py`

## Neighbor Risks
- Cron `Content Draft (war-story)` (`f6efeb7950d4`, 10:00 Tue-Thu) зависит от дедупа тем и checklist-ожиданий до подготовки delivery package.
- Cron `Analytics Loop` (`8be138a2b33f`, 15:00 daily) и `X Tracker Fetch` (`cd9bc007c07a`, 12:00 daily) читают публикационный лог и могут ошибочно трактовать off-pipeline writes.
- `post_with_log.sh` вызывает `operators/operator_pipeline.py`; регресс approval-token, media gate или write counter может открыть путь к публикации без Human Gate либо ложно заблокировать approved post.
- Engagement/follow скрипты делят лимитные инварианты с operators: публичные writes max 3/day, follow max 2/day (hard 3 по AGENTS).

## Known Traps
- `operator_pipeline.read_writes_used_today`, `increment_writes`, `consume_approval_token` имеют глобальные default-path значения, но принимают `Path`; unit-тесты обязаны передавать tmp path и не трогать реальные `data/write_counter.json` / `data/approval.token`.
- `operator_pipeline.main` читает `CONTENT_BRIEF.md`, env и глобальные пути; unit-контур тестирует `approve_post` и path-параметризованные helpers, не CLI side effects.
- `operator_checklist._normalize_account` сохраняет регистр; `operator_account.check_account` тоже case-sensitive после снятия `@`.
- Для `@RobotsTJ500` cover обязателен по умолчанию; только явное `Изображение: нет/no/none` отключает media gate.
- `published_topic_check.fetch_post_texts` вызывает `xurl` через subprocess; unit-контур тестирует только `tokens()` и чистую overlap-логику.
- `loop_guard.Guard` пишет state-файл при `record()` и использует `datetime.now()` / `time.time()`; unit-тесты изолируют `LOOP_DIR` временным каталогом и не тестируют timeout/stale-window без DI.

## Update Rule
Менял verdict-семантику, checklist/account/pipeline/topic/loop guard гейт или их сценарные ожидания — обнови тесты, `scenario_map.yaml` и эту карточку в одном GWT-коммите.

### GIVEN `operators-gate.verdict_contract`
- GIVEN `Verdict.SATISFIED`, `Verdict.NOT_SATISFIED`, `Verdict.INCONCLUSIVE` и `CheckResult` с каждым enum-значением.
- WHEN читается свойство `passes`.
- THEN только `SATISFIED` возвращает `True`; `NOT_SATISFIED` и `INCONCLUSIVE` возвращают `False` как fail-closed контракт для всех operator-гейтов.

### GIVEN `operators-gate.checklist_validation`
- GIVEN draft text, account, parsed brief table fields, required mentions and media values.
- WHEN вызываются `_normalize_account`, `_cyrillic_ratio`, `parse_brief_fields`, `_check_language`, `_check_mentions`, `_check_media`.
- THEN account trim снимает `@` и whitespace, но сохраняет case; Cyrillic ratio дает `0.0`, `1.0` и промежуточное значение; parser читает markdown rows без header/separator; `@RobotsTJ500` RU final блокируется, non-RTJ account skipped; missing mention блокируется; explicit no-media opt-out passes, RTJ default no-cover blocks, existing cover passes.

### GIVEN `operators-gate.account_normalize`
- GIVEN requested account variants and allowed account lists.
- WHEN вызываются `operator_account._normalize_account` и `check_account`.
- THEN `@`/whitespace нормализуются; exact-case allowed account returns `SATISFIED`; lowercase mismatch returns `NOT_SATISFIED`; missing/empty allowed list returns `INCONCLUSIVE`; missing/empty requested account returns `NOT_SATISFIED`.

### GIVEN `operators-gate.pipeline_approval`
- GIVEN `approve_post` inputs with token/account/limits/facts/checklist and tmp-path write counter/token files.
- WHEN вызываются `approve_post`, `read_writes_used_today`, `increment_writes`, `consume_approval_token`.
- THEN valid token + available writes + no numeric facts + media opt-out returns `(True, "all operator gates satisfied")`; missing token blocks at approval; writes=3 blocks at limits; uncovered `2026` blocks at factcheck; missing counter reads `0`, invalid JSON reads `3`, stale date resets to `0`, current date reads stored writes; increment writes supplied path; consume deletes supplied token path.

### GIVEN `operators-gate.topic_dedupe`
- GIVEN draft/topic strings and `MANUAL_THEMES[0]` keyword threshold.
- WHEN вызывается `tokens()` and overlap is computed as set intersection.
- THEN tokens lowercase text, remove stop words and words shorter than 4 chars; recent-post duplicate risk is represented by overlap size `>= 3`; manual gromykoss theme flags at `min_overlap=2` and does not flag one-keyword overlap.

### GIVEN `operators-gate.loop_guard`
- GIVEN `Guard` instances with isolated tmp `LOOP_DIR`, max iteration, budget and human-escalation thresholds.
- WHEN вызываются `check()`, `record()` and `is_duplicate()`.
- THEN `check()` stops at max iterations and budget limit; successful `record()` increments iteration/cost, resets failures and marks item id duplicate; consecutive failed `record()` calls stop the loop at the configured human-escalation threshold.
