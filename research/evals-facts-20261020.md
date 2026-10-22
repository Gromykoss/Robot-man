# Fact-base: evals + observability (депозит Hermes, 21.10) — частично верифицировано robot-man 21.10

## Контракт (canonical)
- `evals/<name>/{dataset.jsonl, scorer.py, eval.yaml}`
- Раннер: `~/.hermes/scripts/eval_runner.py` — stdlib+PyYAML, актуально **225 строк**, sha256 d89ffa7db78975be… (161 — значение на момент подготовки депозита, файл дорос после OTel-фазы emit_otlp; подтверждено Hermes 21.10; мой ast-чек ✓)
- Пайплайн: валидация → run_cmd → пороги из eval.yaml → вердикт-JSON (latest.json + verdict-ts.json) с sha256 датасета/конфига/билда
- Exit-коды: **0=PASS / 2=FAIL / 3=CONFIG**; первая строка stdout — сигнал [PASS]/[FAIL]/[CONFIG]
- kind: agent (блокер агентских деплоев) и kind: service (блокер сервисных)

## Цифры
- **11 гейтов вживлены VERIFIED (20-21.10):**
  1. researcher report-gate
  2. reviewer verdict-gate (переписан по BLOCKER-репорту: dual-ветка JSON/YAML, evidence_rule)
  3. kupi deploy-gate (порог pass_ratio ≥0.96 временный: факт 27 failed / 671 passed / 78 skipped; ужесточить до 1.0 после закрытия F4)
  4. robot-man post-gate (голд-сет 7/7, живой блок-тест rc=2 до X-вызова) — Мой: `~/robot-man/evals/post-gate` существует ✓
  5. rab9 deploy-gate
  6. instagram publish-gate
  7. job-hunter blog-gate
  8. voice bridge-gate (WS-426 сигнатура)
  9. pokupki tbank-gate
  10. default backup-gate
  11. cyberstrike findings-gate
- Fallback — формального eval НЕТ честно: гейт встроен в buzz-send handshake (accepted/VERIFIED). Самотест 5 путей PASS.

## Langfuse → не выбран
- Владелец выбрал вариант 3 (лёгкий OTel-слой), Langfuse отложен
- Observability: OTel collector contrib 0.163.1 на 127.0.0.1:4317/4318 → spanmetrics (dimensions eval.name/eval.kind/eval.verdict) → Prometheus :8889 → Grafana дашборд **Evals-Gates** (/d/evals-gates)
- Телеметрия раннера env-gated (EVALS_OTLP_ENDPOINT, off по умолчанию), best-effort — exit-коды не меняются (selftest 5 путей baseline/after IDENTICAL); file-аудит спанов (eval-traces.json в docker-томе)
- E2E: спан → traces_span_metrics_calls_total{eval_verdict=PASS} в Prometheus (series=1) → Grafana datasource health OK
- Вывод Hermes: каждый гейт замеряем как метрику (вердикт + длительность) без тяжёлого Langfuse-стека; апгрейд к Langfuse позже поверх того же OTLP

## Верифицировано мной
- eval_runner.py существует, валидный Python ✓ (но 225 строк vs 161 в депозите — фикс расхождения до драфта)
- `~/robot-man/evals/post-gate` существует ✓
- 11 гейтов / Grafana / Prometheus — self-report Hermes; до драфта выборочно: мой post-gate прогон eval_runner'ом, curl Prometheus series

## Угол для поста
«Гейты как код: 11 eval-гейтов флота, один 225-строчный раннер, exit-коды вместо доверия + OTel-слой вместо Langfuse» — идеальная пара к посту памяти (та же философия: механика вместо доверия).
