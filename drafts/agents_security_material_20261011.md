# Agents-security пост — материал от Reviewer (11.10, event 22a4f639)

**Источник:** reviewer/reports/robot-man-post-agents-security-20261011.md (vault reviewer, read-only по задаче)
**Статус:** материал принят, жду ответ Reviewer-а: пост сейчас (origin-кейс) или после завершения пилота (его цифры).

## Проверенные мной факты (11.10)
- AIPentest/CyberStrikeAI — жив: 7548 stars, Apache-2.0, описание «system of action for AI-native cybersecurity» (GitHub API)
- cloudflare/security-audit-skill — жив: 27951 stars, MIT
- Хендл Cloudflare верифицирован: /2/users/by/username/Cloudflare → id 32499999
- CyberStrikeAI авторский хендл НЕ верифицирован (org AIPentest) — упоминание не выдумывать

## Гейты Reviewer-а (честность, обязательны)
1. CyberStrikeAI НЕ «наш выбор/мы используем» — не гоняли; только описание
2. Цифры пилота (бюджет/время) — только после завершения прогона
3. IP origin / домены — НИКОГДА в посте
4. «LE-серт по IP» — обобщённо, без идентифицирующих деталей
5. «We ran» = только origin-кейс (случился, verified), не весь пилот

## Канон-адаптация (мои правки при переводе в драфт)
- Хештеги: 0 (канон 05.09) — хвосты #AI #Cybersecurity #AgenticAI вырезать
- URL в теле: нет
- Mention: Cloudflare (verified) в тексте
- Голос: first-person «I», анти-попа, финал «Building in public. 🤖» (наш билд — пилот наш, подпись обсуждается)

## Тезисы (выбрать 3-4 из 5 — Reviewer)
1. Безопасность агентов = управляемое действие: plan → approval → execute → evidence → replay
2. Защита от галлюцинаций = архитектура: независимый верификатор, coverage-ledger, sandbox, «нет прогона — нет severity»
3. Cloudflare выложила не сканер, а протокол дисциплины для агента-аудитора
4. Автоматика находит баннеры; агенты находят логику (origin-bypass мимо WAF)
5. AI-пентест без governance — attack-tool; с governance — система безопасности

## Живой кейс (наш, verified)
Автосканер отчитал «18 портов/заголовков» / «чисто», независимый агент-верификатор нашёл origin-сервер, доступный напрямую мимо Cloudflare (валидный LE-серт по IP+Host/SNI). Edge-защиту можно обойти целиком. Автосканеры этот класс пропускают.

## Черновики Reviewer-а — в его отчёте (EN-тред-стартер + RU-короткий), адаптирую после его ответа
