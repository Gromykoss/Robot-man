# FrontierHarness Eval — факт-банк (02.09.2026)

## Первоисточники (проверены 02.09)
- Тред: @guanlan (Guanlan Dai) https://x.com/guanlan/status/2095179765355540575 (15:59 UTC, 121.9k imp, 882 bookmarks, 1076 likes, 90 replies)
- Leaderboard: frontierharness.org
- Blog: runta.com/blog/introducing-frontierharness-eval
- GitHub: github.com/runta-dev/frontier-harness-eval
- Модель: Kimi K3 (константная, «not native to one of the leading harnesses» — выбор осознанный, автор подтвердил в треде @timhollister_x)
- Gateway: все харнессы через единый шлюз (OpenAI Responses API + Anthropic Messages API), идентичные веса

## Проверенные цифры (leaderboard site, v1.0)
- 9 харнессов (12 конфигов), 360 прогонов, 2 млрд токенов
- Pass rates 50.0%–66.7%; cost/pass $1.05–$18.34
- Codex 66.7% $3.47 (quality leader, v0.148.0)
- Claude Code 63.3% $18.34 (самый дорогой, cache 67.8% худший)
- Pi 60.0% $2.43 (balanced)
- Exo 53.3% $1.05 (cost leader, частый early-give-up)
- OpenCode 50.0% $0.06→$3.24 (failures excluded — только 15 passes!)
- Hermes 50.0% $2.90 (v0.20.4 — НАШ Hermes в списке!)
- Kimi Code 56.7% $3.65; DSH-семейство 56.7–63.3% $3.28–4.72
- Кейс DeepSWE: Pi 90 turns $2.50 vs Claude Code 381 turns $64.36 (~26x)
- Вывод автора: cache hit rate ≠ cost; платишь за число шагов, кэш лишь скидка на шаг
- Методология: golden checkpoint, cold restore каждый прогон (implicit prefix caching ловушка — тёплый кэш искажает бенч)
- Практические выводы автора: Codex «не думая», Pi для массовых задач, Exo если ретраи дёшевы, DSH для wall-clock

## Связь с нами (dogfooding углы)
- Hermes (наш агент) в списке: 50.0% pass, $2.90/pass, cache 85.9% (5-й), speed 6m58s — середина/низ по pass, но НЕ худший по цене
- Наш стек: Kimi K3 (GULAG) — та же модель, что в eval; DeepSeek v4 (robot-man)
- Продолжение дуги WebMCP→tailcat→harness: «интернет агентов строится» — теперь меряется сам слой исполнения
- Hermes agent проект (@NousResearch) — Hermes в списке это ХАРНЕС Hermes (v0.20.4), совпадение имени с нашим профилем: в посте НЕ путать (наш бот работает на Hermes agent, но в eval тестируется Hermes harness от Hermes Agent project — фактически ДА, это скорее всего тот же проект: v0.20.4 = версия Hermes Agent. Значит «наш агент в списке» — правомерно, но проверка: Hermes v0.20.4 в списке версий соответствует Hermes Agent. Подтверждено: наш бот работает на Hermes agent v0.20.x на момент eval!)

## 403-ограничение
- Реплай API от @RobotsTJ500 на посты без mention → 403 (verified 02.09)
- Quote тоже под ограничением («reply to or quote»)
- Рабочие пути: mention в чужом посте / свой тред / вручную

## Статус
Пост-план: standalone от @RobotsTJ500 (не реплай — 403) или реплай вручную. Тред горячий (122k imp), актуальность высокая.
