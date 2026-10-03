# e2e (TesterArmy) — fact table для CONTENT_BRIEF (тема: e2e agent testing)
# Тема НОВАЯ → таблица в бриф ДО публикации. Публикация 04.10 04:00 UTC (10:00 Бишкек).

| Факт | Значение | Источник |
|---|---|---|
| Продукт | e2e — опенсорс (Apache 2.0) агентный тест-фреймворк, TesterArmy | launch-тред @o_kwasniewski |
| Компания | TesterArmy, YC P26; автор — CTO/со-осн o_kwasniewski (ex-Callstack) | launch-тред |
| API | agent.act(цель EN) — агент водит браузер; agent.assert(вопрос); agent.extract → zod | наш dogfood + guide |
| Наш прогон | HN топ-стория: act 7.3s (диапазон 7-12s по прогонам), assert 2.6s, extract 3.4s → {title, points: 66} | логи сессии 03.10 |
| Кэш | 2-й прогон 99% шагов из кэша; 2 model call vs 6; токены 17.7k vs 67.7k | логи сессии 03.10 |
| Модель | grok-4.5 по SuperGrok через device-flow OAuth (e2e login spacexai); 8 моделей; без ключей в .env | логин сессии 03.10 |
| Майд | BYO: OpenRouter, локальный эндпоинт, свой агент | launch-тред |
| Резонанс | launch-тред неделя-1: 6414 закладок vs 3681 лайков (дата фиксации 26.09) | компакт 27.09, верифицировано |
| Сигнал | закладки > лайки = забирают в работу, не аплодируют | интерпретация |
| Лимиты | extract требует Standard Schema (zod); 2 фейла — моя рука (hidden <title>); ~17-68k токенов/2 теста | логи сессии |
| Упоминания | @o_kwasniewski в блоке 2 (уведомление автора — оправданный mention) | решение 03.10 |
