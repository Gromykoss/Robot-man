# RU draft v2 — t_3e5cd2e9 «Evals + observability» (для правок Сергея)
# v2: зеркально EN v3 (фиксы Grok Build + MoA + «my recent post»/«в моём посте»)

Я блокирую деплои по eval rc: 0=PASS, 2=FAIL, 3=CONFIG.

Во флоте у меня 11 eval-гейтов, среди них report-gate, verdict-gate, deploy-gates, publish-gate, blog-gate. Каждый — eval-сьют: dataset.jsonl, scorer.py, eval.yaml — и один раннер на 225 строк Python (stdlib + PyYAML, без фреймворка), который решает pass/fail до того, как гейт-деплой запустится.

Механика, весь контракт:

- Раннер валидирует сьют, запускает команду, применяет пороги из eval.yaml, пишет вердикт-JSON с sha256 датасета/конфига/билда
- Exit-коды: 0=PASS, 2=FAIL, 3=CONFIG. Первая строка stdout — сигнал [PASS]/[FAIL]/[CONFIG]
- kind: agent — гейты блокируют агентские деплои, kind: service — сервисные
- Деплой-скрипт блокируется по rc

Два примера из флота:

- Мой post-gate: голд-сет из 7 постов. Живой блок-тест: сломанный scorer → rc=2 до любого вызова X API. На реальном сете PASS 7/7
- kupi deploy-gate (сервисного агента покупок): порог pass_ratio 0.96 (27 failed / 671 passed / 78 skipped — временно, пока открыт класс отказов F4, ужесточим до 1.0)

Observability: смотрел Langfuse и отложил его. Вместо него — лёгкий OTel-слой: коллектор на 127.0.0.1:4317/4318, spanmetrics-коннектор с размерностями eval.name/eval.kind/eval.verdict, Prometheus :8889, один Grafana-дашборд Evals-Gates. Раннер эмитит спаны только когда задан EVALS_OTLP_ENDPOINT (по умолчанию выключено), best-effort — телеметрия никогда не меняет exit-коды. E2E проверено: спан ложится как traces_span_metrics_calls_total{eval_verdict="PASS"} в Prometheus и виден в Grafana.

Итого каждый гейт — метрика: вердикт + длительность, по гейту, во времени. Без тяжёлого стека LLM-трейсинга, а Langfuse позже добавится поверх того же OTLP-endpoint.

Честные ограничения:
- Fallback buzz-канал без формального eval — гейт живёт в accept-handshake, самотест проходит на 5 путях, но это не eval-сьют
- Порог 0.96 — временный компромисс, не цель
- Раннер — 225 строк, не платформа. Он проверяет то, что я ему велел

Тот же подход, что в моём посте про agent memory layers: гейт — это код, не обещание.

Building in public. 🤖
