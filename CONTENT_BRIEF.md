# CONTENT_BRIEF — пост t_3e5cd2e9 «Evals + observability» (23.10.2026)

| Поле | Значение |
|---|---|
| Тема | Eval-gate как дисциплина деплоя: 11 гейтов, раннер 225 строк, OTel-observability |
| Статус | одобрен владельцем 23.10 («публикуй») |
| Изображение | /home/hermes-workspace/robot-man/drafts/cover_evals_v2.png |
| Mentions | нет — сторонние хендлы в тексте отсутствуют |
| Язык | EN |

## Факты (источник: research/evals-facts-20261020.md — 225 строк, sha256 d89ffa7db78975be… сверен 22.10; post-gate [PASS] rc=0 живьём; Prometheus series живы)

| Токен | Факт | Источник |
|---|---|---|
| 0 / zero | exit-код 0 = PASS; refusal=0 N/A | factbase ✓ |
| 2 | exit-код 2 = FAIL | factbase ✓ |
| 3 | exit-код 3 = CONFIG | factbase ✓ |
| 1 | 127.0.0.1 collector; one runner | factbase ✓ |
| 11 | число eval-гейтов во флоте | factbase ✓ |
| 225 | строк Python-раннера (stdlib + PyYAML) | factbase ✓ |
| 96 | pass_ratio threshold 0.96 (kupi deploy-gate, временный) | factbase ✓ |
| 27 | failed / 671 passed / 78 skipped (kupi) | factbase ✓ |
| 671 | passed-строк kupi | factbase ✓ |
| 78 | skipped-строк kupи | factbase ✓ |
| 127 | OTel collector 127.0.0.1 | factbase ✓ |
| 4317 | OTLP gRPC порт | factbase ✓ |
| 4318 | OTLP HTTP порт | factbase ✓ |
| 8889 | Prometheus spanmetrics порт | factbase ✓ |
| 7 | золотой сет из 7 постов (post-gate) | factbase ✓ |
