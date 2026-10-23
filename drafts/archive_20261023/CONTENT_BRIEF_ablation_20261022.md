# CONTENT_BRIEF — пост «A/B: abliterated GLM-5.3 vs stock» (22.10.2026)

| Поле | Значение |
|---|---|
| Тема | A/B пилот: abliterated GLM-5.3 vs базовый — 0 отказов у обеих; вердикт fallback |
| Статус | одобрен владельцем 22.10 («пости», тема горячая) |
| Изображение | /home/hermes-workspace/robot-man/drafts/cover_ab0_20261022_v1.png |
| Mentions | нет для реплаев-ответов; хендлы в тексте основного поста уже опубликованы и разрезолвлены |
| Язык | EN |

## Факты (источники: отчёт CyberStrike + сырые артефакты ~/robot-man-artifacts/pilot-abliterated/ — верифицировано мной 22.10; TechCrunch 03.09; Reddit)

| Токен | Факт | Источник |
|---|---|---|
| 10 / ten | 10 defensive/red-team промптов на обе модели | отчёт; артефакты (21 row) ✓ |
| 0 / zero | отказов A 0/10, B 0/10 | артефакты: refusal=0 ×20 ✓ |
| 4.95 | качество A (mean) | артефакты ✓ |
| 4.80 | качество B (self-score, оштрафован) | отчёт ✓ |
| 31.5 / 8.2-69.4 | латентность A ср (мин-макс) | артефакты: values ✓ |
| 5,157 / 5157 | chars A mean | артефакты ✓ |
| 2,371 / 2371 | chars B mean | артефакты ✓ |
| 2.2x | A многословнее | расчёт 5157/2371 ✓ |
| $0.19 / 0.19 | A-side cost per-row (sum 0.1857) | артефакты ✓ |
| $0.38 / 0.38 | полный пилот по usage-логу (вкл. run1 + refusal probe) | отчёт |
| $5 / five | prepaid баланс | отчёт |
| 16k | output cap A (reasoning) | отчёт |
| $20 / 20 | подписка Developer = $0 кредитов | Reddit r/opencodeCLI |
| $900 / 900 | юзер сжёг при контексте >150k | Reddit r/opencodeCLI |
| 150k | контекст-порог | Reddit |
| September / September | TechCrunch о старте (03.09) | techcrunch.com |
| GLM-5.3 | база (z.ai) | отчёт |
| pynput | кейлоггер базовой модели в refusal-прогоне | отчёт |
| 2,200-char / 200 / 2,200 / 2200 | Layer 0 cap per profile; pgvector HNSW max 2000; gemini-embedding-001 1536 dims; 9 profiles | канон памяти 19.10; пилот 21.10 |

