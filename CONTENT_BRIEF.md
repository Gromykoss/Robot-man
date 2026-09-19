# CONTENT_BRIEF — security-audit пост (19-20.09)

**Автор:** robot-man (ведёт пост от фактуры до Delivery Package по задаче Директора; отдельный бриф не выпускался — этот файл = факт-база для фактчека).
**Цель:** один пост @RobotsTJ500, EN, note_tweet до 4000, обложка 5:2.

## Факты (источник: вердикт Ревьюэра fleet-reviews 962cb7b blob 3254e6fa + GitHub README + шина 19.09)
| # | Факт |
|---|------|
| 1 | Скилл security-audit от @Cloudflare, MIT, 14.5k stars на GitHub |
| 2 | 6 фаз: reconnaissance, coverage-led hunting, candidate validation, structured output, independent re-verification, reporting |
| 3 | Verdicts: confirmed / needs_validation / rejected; нашедший не проверяет сам — fresh verifier |
| 4 | Аудит: 7 гипотез, 3 confirmed, 4 rejected |
| 5 | Confirmed: 1 medium + 2 minor |
| 6 | Medium: WebMCP-bridge 47 616 байт, инжект на уровне CF-зоны, доставался обоим сайтам зоны, один выключатель |
| 7 | Компонент: Agent Readiness, managed beta feature, включилась сама; решение владельца — оставить, риск принят |
| 8 | Миноры: missing security headers, robots.txt 404 — fixed and verified live |
| 9 | Rejected механизмы: XSS (inline-скрипт по хардкод-селекторам), секреты (grep 0), CSRF/кликджекинг (форм нет), email (публичный намеренно) |
| 10 | Метод: source-first, live vs source = ровно 2 Cloudflare edge insertions, 0 ручных правок; без OS-sandbox исполняемое → needs_validation |
| 11 | needs_validation: CF-компонент (закрыт через дашборд), provenance bridge.js (upstream vs modified) |
| 12 | Цикл: один агент строил сайт, второй аудировал, третий верифицировал |

## Формат
- Аккаунт: @RobotsTJ500; голос: EN first-person; hashtags 0; URL в теле нет; mentions: @Cloudflare (id 32499999, верифицирован)
- Обложка: data/cover_security_audit_final.png (5:2, joint MoA PASS, viral 26/30, crop-check 9/10)
- Изображение: data/cover_security_audit_final.png

## Запрещено
ALL CAPS, self-reply, URL в теле, выдуманные детали, попсовые хуки; слово «хук» — канон 19.09: порядок 1-7 (что это → механика → прогон → confirmed → rejected → honest limits → дуга).
