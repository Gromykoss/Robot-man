# Аудит operator-слоя robot-man — статус 03.09.2026

> Было: 15.08.2026 — правила только в промпте, `post_with_log.sh` дырявый.  
> Сейчас: operators подключены + ревизия Delivery Package / cover hard-block (03.09).

---

## Исполняемый publish path

```
post_with_log.sh
  → export POST_IMAGE
  → python -m operators.operator_pipeline  (approval, limits, account, factcheck, checklist)
  → cover hard-block (no image → exit 1 unless ALLOW_TEXT_ONLY=1)
  → xurl-post-guard media-upload + post
  → increment write counter + consume approval.token
  → published_posts.jsonl
```

## Operators (код)

| Модуль | Правило | Статус 03.09 |
|--------|---------|--------------|
| `operator_approval.py` | Human Gate: нужен approval token | ✅ BLOCK без токена |
| `operator_limits.py` | writes/day | ✅ |
| `operator_account.py` | только RobotsTJ500 по умолчанию | ✅ |
| `operator_factcheck.py` | цифры vs brief lines | ✅ (грубо: весь brief как blob) |
| `operator_checklist.py` | EN-only final; mentions; **cover default required** | ✅ cover hard (opt-out: Изображение=нет) |
| `post_with_log.sh` | cover path required | ✅ text-only fallback удалён |

## Промпт-канон (не код, но обязательно)

| Правило | Где | Статус 03.09 |
|---------|-----|--------------|
| RU-first draft | VOICE_PROFILE, content-writer, AGENTS | ✅ канон; код не enforced на draft-этапе |
| Show cover before ok | Delivery Package Gate | ✅ промпт; MEDIA в чат |
| No autonomous ship | x-posting-workflow | ✅ AUTONOMOUS MODE 13.07 **удалён** |
| Anti-ad / no ALL-CAPS | VOICE_PROFILE, joint-moa | ✅ |
| Absorb Sergey edits | skill `sergey-edit-absorb` | ✅ |

## Что всё ещё НЕ в коде (осознанно / backlog)

- RU-first на этапе драфта (нет CI на `drafts/`) — process gate
- Joint MoA anti-ad — LLM checklist, не deterministic
- Factcheck токены vs structured fact-table — всё ещё line-blob brief
- Прямой `xurl` write минуя post_with_log — частично закрыт root guard / изъятыми write-creds

## Историческая ошибка (не повторять)

Аудит 15.08 писал «approval только в промпте». После появления `operators/` этот абзац **устарел**. Этот файл — актуальный статус.

## Связанные файлы ревизии 03.09

- `VOICE_PROFILE.md` (полный rewrite)
- `AGENTS.md` gates 3a/3b + process
- `post_with_log.sh`, `operators/operator_checklist.py`
- skills: content-writer, x-posting-workflow, joint-moa-protocol, post-quality-gate, sergey-edit-absorb
