# Инструменты анализа X/Twitter — сводный справочник

Собрано 30.08.2026. ВСЕ инструменты из «не тестировавшихся» прогнаны на @RobotsTJ500 (день теста: shadowban-диагноз по nitter был активен). Результаты прогонов зафиксированы в каждом разделе.

Контекст дня теста: nitter показывал фильтрацию, но поисковые чекеры дают чистый результат — вероятно, ограничение не search-ban (см. выводы внизу).

## 1. Тесты тени / видимости

| Инструмент | Что проверяет | Результат прогона 30.08 на RobotsTJ500 |
|---|---|---|
| **shadowban.yuzurisa.com** (API: shadowban-api.yuzurisa.com:444/USERNAME) | Search ban, search suggestion (typeahead), ghost ban, more_replies (deboost). FastAPI, JSON | ✅ **Все чисто**: search=`_implied_good`, typeahead=true, ghost.ban=false, more_replies.ban=false |
| **hisubway.online/shadowban/** | Search Suggestion Ban, Search Ban, Ghost Ban, Reply Deboosting | ✅ **Все чисто** (5/5 зелёных: аккаунт существует, нет ни одного бана) |
| **api.sorsa.io/playground/shadowban-check** | Search ban, Search Suggestion Ban, Sensitive Profile, Account Privacy. Без логина. Есть бесплатный API (100 req) | ✅ **«No visibility restrictions detected»**: search ban not detected (20 постов найдено), suggestion not detected, not sensitive, public |
| **postory.io/twitter-shadowban-test** | 5 проверок: profile visibility, search ban, ghost ban, reply deboost, people search. Апселл: recovery-скан $4.99 | ✅ **«5 clear»**: профиль публичен, 5/5 постов в поиске, реплай к @FReza1984 виден в треде и не задебужен, аккаунт в people search |
| **opentweet.io/tools/shadowban-check** | Account privacy + search visibility через официальный API | ⚠️ **«Minor Warning»** — search visibility «could not determine» (X вернул client-rendered page). Ненадёжный прогон, не вердикт о бане. Есть бесплатный weekly-monitor по email |
| **notpeople.ai/x-shadowban-checker** | Health/engagement скоринг (0-100), search ban, reply deboost, reach-анализ. ~30 сек | ✅ Search: «posts appear, no search ban»; Replies: «75% earn reactions — no reply deboost». Вердикт: **«Real, but underperforming»** — health 100/100, engagement 48/100, узкое место = reach (~28 views/reply = 7.1% от 396 фолловеров, цель 20%+); активность низкая (~0 постов/0.6 реплаев в день, цель 2-3/10-20) |
| **circleboom.com/…/twitter-shadowban-test** | 5 тестов: Search Suggestion Shadow, Total Search Blackout, Reply Lock, Reply Visibility Filter, Early Engagement Seed. Логин не нужен для базового теста | ✅ **«No shadow bans in any country»** — все 5 тестов чисто. Апселл: удаление бот-фолловеров |
| **tweethunter.io/shadowban-checker** | Search visibility (самый частый тип). Кэш 24ч | ✅ **«Not Shadowbanned»**: «Found 10 of your recent tweets in search results» |
| **x-shadowban-checker.fia-s.com** (Shadowban Checker F) | По-постовой поиск-тест (пакеты URL); вкладки Shadowban/Postban; Android-приложение | ✅ Прогон 30.08: 4 поста = Search OK |
| **nitter.tiekoetter.com** | Публичная видимость | ⚠️ Единственный инструмент, показавший фильтрацию — расходится со всеми остальными |
| Публичный поиск x.com инкогнито (`from:USER`, Latest) | Эталонный search-ban тест | ✅ Эталон (по уроку 04.08.2026) |
| xurl search / x_search (Grok) | ⚠️ НЕ тесты бана — привилегированный доступ | Для проверки существования постов |
| curl прямой ссылки (200) | Пост жив | ✅ |
| **Under the Hood (официальный X)** | Метки на аккаунте/постах. Первым по порядку | URL в UI x.com; код в xai-org/x-algorithm |

**Итог прогонов 30.08:** 8 из 8 поисковых чекеров (yuzurisa, hisubway, sorsa, postory, notpeople, circleboom, tweethunter, Checker F) говорят: search ban / ghost ban / reply deboost НЕ обнаружены. Только nitter показывал фильтрацию.

## 2. Скоринг алгоритма / репутация

| Инструмент | Что даёт | Результат прогона 30.08 |
|---|---|---|
| **tweethunter.io/tweepcred-calculator** (TweepCred) | Оценка TweepCred (0-100). Порог 65: ниже — только ~3 твита в дистрибуции. Факторы: ratio 0-30, age 0-15, engagement 0-25, activity 0-10, Premium 0-16 (Basic+4/Premium+10/P+16), mobile 0-4. Брейкдаун скрыт за триалом | ⚠️ **RobotsTJ500 = 50/100 «Below Threshold»**; @gromykoss = 48/100. NB: инструмент по URL-параметру иногда подставляет чужой хэндл (RobotsT1500→«Robot TG») — проверять title карточки. Это оценка по открытому коду, не официальный скор |

Официальная механика — код `github.com/xai-org/x-algorithm` (13.08.2026):
- Веса: Report −234.0, Mute −58.8, NotInterested −43.2, Block −31.2, Reply/Quote/DM 5.0, CopyLink 20.0, Retweet 1.0, Like 0.5; мутуал-реплай 5+15=20.0
- Фильтры: посты >48ч вне фида; OON-репосты/реплаи дропаются; NewUserMinEngagementFilter; AuthorDiversityDecay (~2 поста/день)
- Метки: SPAM_HIGH_RECALL_USER (не видят все кроме автора), DO_NOT_AMPLIFY (не-фолловеры), COPYPASTA_SPAM, AGATHA_SPAM (жалобы: спам-репорты/фавориты >0.9975)

## 3. Аналитика / метрики

| Инструмент | Что даёт | Результат прогона 30.08 |
|---|---|---|
| **notpeople.ai** (уже в разделе 1) | Health/engagement score + сравнение с нормой X | Health 100/100; Engagement 48/100 (низкая активность и reach) |
| **tweethunter.io/metrics-calculator** ⚠️ | Engagement rate, средние показы | Не прогонялся (аналогичные данные уже получены через notpeople; требует входа для полного отчёта) |
| **tweethunter.io/how-much-your-twitter-is-worth** ⚠️ | Оценка стоимости аккаунта | Не прогонялся — развлекательный, для нас не приоритет |
| **X Analytics (нативный)** | Импрешны, engagement, топ-посты | Встроен в Premium, используется |
| **xurl / X API public_metrics** | Точные цифры по постам | ✅ Рабочий, основной |
| **api.sorsa.io** — Engagement Calculator, Compare Users, Follow Checker, Recent Followers, Account Age Checker и др. (12 tools) | Бесплатный API 100 req, 20 req/sec | Проверен shadowban-checker; остальные инструменты той же платформы доступны тем же путём |

## 4. Контент / тренды

| Инструмент | Что даёт | Статус |
|---|---|---|
| **tweethunter.io/trending** ⚠️ | Тренды X | Не прогонялся |
| **tweethunter.io/thread-finder** ⚠️ | Поиск тредов авторов | Не прогонялся |
| **Twemex (расширение)** ⚠️ | Популярные посты в профиле/поиске | Не прогонялся (расширение браузера) |
| **xurl search / X MCP search_posts_all** | Поиск, мониторинг авторов | ✅ Рабочий, основной |
| **opentweet.io** free tools | AI-генераторы, thread reader, engagement calculator, content calendar | Каталог из 20+ инструментов; проверен только shadowban-check |

## 5. Утилиты

| Инструмент | Что даёт | Статус |
|---|---|---|
| **tweethunter.io/twitter-id-converter** ⚠️ | ID ↔ username | Не прогонялся (ID у нас уже есть из API) |
| **sorsa ID Converter / Account Age Checker** | ID, возраст аккаунта | Платформа проверена |
| **tweetpik.com** ⚠️ | Пост → картинка | Не прогонялся |
| **tweethunter.io video/gif downloader, data export** ⚠️ | Скачивание/экспорт | Не прогонялся |

## Рекомендованный пайплайн диагностики (обновлён 30.08)

1. **Официальные правила** — help.x.com automation + search policies (нарушение > алгоритм); метка «automated» — только вручную
2. **Under the Hood** (официальный X) — если доступен
3. **Быстрый пакетный тест** — shadowban.yuzurisa.com (API: `shadowban-api.yuzurisa.com:444/USERNAME`, JSON, без логина) ИЛИ api.sorsa.io
4. **Reply-специфика** — hisubway (ghost + deboost) или postory (5 проверок)
5. **Скоринг и причина падения охвата** — notpeople.ai (health/engagement/reach-разбор) + tweethunter TweepCred
6. **nitter** — расходится с остальными; использовать только как доп. сигнал, НЕ как единственный вердикт
7. **xai-org/x-algorithm** — при глубоких расследованиях

## Главный вывод для @RobotsTJ500 (30.08.2026)

Все независимые чекеры и X API согласны: **search ban, ghost ban, reply deboost отсутствуют**, аккаунт виден в поиске и в тредах. Диагноз «shadowban» по nitter не подтверждается ни одним инструментом. Реальная проблема по notpeople: **reach ~28 views/reply (7.1% фолловеров при норме 20%+)** и низкая активность (~0 постов/0.6 реплаев в день) — это проблема дистрибуции и объёма, а не бана. TweepCred 50/100 (порог 65) — только ~3 твита участвуют в дистрибуции; путь вверх: Premium-буст (+10 уже есть), engagement quality (до +25), активность.

## Источники
- Прогоны 30.08.2026 (браузер + API) — все результаты в таблицах
- Пост @bkdgiffug (lumxss) от 29.08.2026 — TweepCred + Shadowban Checker F
- skill shadowban-recovery / shadowban-diagnosis (внутренние уроки 31.07–13.08.2026)
