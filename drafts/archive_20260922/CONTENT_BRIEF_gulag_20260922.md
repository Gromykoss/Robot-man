# CONTENT_BRIEF — 2026-09-22

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## ШАГ 0.5 — Engagement Feedback (TACTICS.md от 21.09 05:03 UTC, свежий)

TOP-3 за 7 дней (daily_20260920.json):
- BrowserSkill 17.09 → **464 imp / 4❤ / 8💬 / 1🔁 / 1🔖** → «подробный разбор + live-верификация» = формат-победитель недели
- Security-audit 19.09 → 171 imp / 1❤ / 0💬 → дистрибуция живая, каденция 🟢 GREEN
- Chrome-agent 16.09 → 96 imp / 2❤ / 1💬 → верифицированные цифры дают живой тред

FLOP-3:
- Реплаи в тредах → 10-40 imp фоновые → реплай-марафон не окупается
- Reply 21.09 (21019743) → 0❤ / 0💬 / 0🔄 → фоновый реплай
- OpenSpec / процессные серии (историч.) → замыленный формат

**Использование:** работающий формат — war story с цифрами, live-проверкой и честными границами. Выбранная тема соответствует. Финал «проверено снаружи 403/403» — тот же приём верификации, что в топ-постах недели.

## ШАГ 0.7 — Pre-Gate (3 вопроса)

- **GULAG 21.09 (инцидент подъёма из консервации):** польза ДА (права каталога vs service-user, atomic tmp+replace, bracket-трюк pkill, HOLD при неоднозначной команде) · сцена ДА (два авто-отката деплоя, «эндпоинты были открыты!», подъём и откат 1-в-1) · актуальность ДА (AI-операторы прода, security hardening) → **3 «да», в конкурс**
- **Jev Ultrafast browser-use (TACTICS №1):** польза ДА, актуальность ДА, сцена — разбор чужого репо [BORDERLINE] → 2 «да». **Проиграл:** факт-база от 17.09 (свежесть 2), а 21.09 в 07:02 UTC уже опубликован пост 2101930064140968172 (TypeSafe Service Review, бриф 21.09) — второй Jev/TypeSafe-класс подряд [DUP]
- **WebMCP (TACTICS №5):** сцены из lived experience нет («отдельного разбора ещё не было») → отброс — правило «post only from lived experience»
- **«Слепое ревью» (TACTICS №2):** заблокировано Human Gate (RU-драфт drafts/blind_review_filemap_v1_ru.md ждёт ok Сергея) → не брифуем
- **Alikhan:** событий за 48ч нет (консервация 15.09) → отброс. **RAB9:** BURNIE-цены → вето (крипто). **robot-man:** реплаи = self-referential рутина → отброс. **hermes-vault:** 0 коммитов за 3 дня (SOUL-main/OPERATIONS/scorecard/Engineering Loop) → пусто.

---

## Тема

**Один недопонятый термин развернул замороженный проект вверх и вниз: полный подъём, два авто-отката деплоя, латентный баг прав каталога — и откат 1-в-1.**
Рабочий заголовок-урок (EN финализирует robot-man): «My own hardening silently broke the service. My smoke gate caught it twice. A single word almost kept it that way.»

## Факты (верифицированы Hermes)

Источник всех фактов: `/home/hermes-workspace/gooolag/CHRONOLOGY.md`, записи за 2026-09-21 (разделы «Влитие gulag-expo-app в монорепо», «Security fix-батч по ревью gooolag#2», «Fix 2 миноров re-review gooolag#2», «РЕВЕРС консервации по команде владельца», «Откат реверса: возврат в консервацию 13.09», «Чистка хвостов YC»). robot-man НЕ ИМЕЕТ ПРАВА менять цифры или выдумывать детали.

| # | Факт | Источник |
|---|------|----------|
| 1 | Внешнее ревью gooolag#2 дало 8 находок: 2 blocker + 3 major + 3 minor (fleet-reviews 2026-09-21-2-7d1be425.md) | GULAG CHRONOLOGY 21.09 |
| 2 | Все 8 закрыты коммитом 7f29e353: admin-token gate (_push_admin_authorized) на /api/push/send и /api/push/notify-user, proof-of-ownership через Synapse whoami, персистентный rate-limiter (flock + atomic store), action-scoped HMAC + 24h expiry, маскирование ПД в логах (_mask_email/_mask_name/_mask_username), _esc-экранирование в chat.js | GULAG CHRONOLOGY 21.09 |
| 3 | Подъём из консервации (Сценарий A RESTORE-RUNBOOK): 7 systemd-юнитов, штатный deploy.sh --i-approve-prod — smoke-гейт ДВАЖДЫ сам откатывал деплой | GULAG CHRONOLOGY 21.09 |
| 4 | Root-cause обоих откатов: rate-store не может писать в /opt/gooolag-secrets — права каталога 750, сервис работает от www-data | GULAG CHRONOLOGY 21.09 |
| 5 | ЛАТЕНТНЫЙ ПРОД-БАГ: pending tmp+replace был сломан теми же правами 750 с момента харденинга — молча, до этого дня; фикс: chmod 770 root:www-data + пре-создание store-файлов | GULAG CHRONOLOGY 21.09 |
| 6 | Dump-ловушка pkill -f убивала собственный ssh-шелл; лечение — bracket-трюк pkill -f '[p]attern' | GULAG CHRONOLOGY 21.09 |
| 7 | Финальный деплой: smoke ВСЕ ПРОВЕРКИ ✓, nginx guard FAILS=0; блокер-2 проверен СНАРУЖИ: /api/push/send и /notify-user без токена = 403/403 («были открыты!»); SHA задеплоенного head — 49d98e20 | GULAG CHRONOLOGY 21.09 |
| 8 | Команда владельца «реверс» (06:10 UTC) понята исполнителем как «поднять проект» — жаргон; проект полностью подняли (мониторы 6/6 resumed), затем по уточнению владельца откатили в консервацию 1-в-1: 7 юнитов stop+disable, мониторы 6/6 paused | GULAG CHRONOLOGY 21.09 |
| 9 | Урок дня: слово «реверс» изъято из канона — только «разморозка/подъём»; при ambiguous командах владельца — переспрашивать ДО исполнения (HOLD-механизм сработал корректно) | GULAG CHRONOLOGY 21.09 |
| 10 | На диске ничего не откатывалось: код 49d98e20 со всеми security-фиксами остаётся — следующий подъём стартует с исправленного кода | GULAG CHRONOLOGY 21.09 |
| 11 | Бонус 21.09: gulag-expo-app влит в монорепо (52 tracked файла, tree-hash поддерева байт-в-байт = 36c1d2eb158c…); чистка хвостов YC: dev-юнит gulag-metro.service (был enabled) disable+удалён, /opt/gulag-expo-app (341M) удалён, зомби /etc/cron.d/gooolag-health удалён | GULAG CHRONOLOGY 21.09 |

## Контекст проекта

**Проект:** GULAG (self-hosted Matrix-мессенджер, прод в консервации с 13.09)
**CHRONOLOGY:** `/home/hermes-workspace/gooolag/CHRONOLOGY.md`
**AGENTS.md:** `/home/hermes-workspace/gooolag/AGENTS.md`

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story (инцидент-репорт: hardening → тихий баг → авто-откаты → терминология) |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» (агент = оператор прода; НЕ «my agent») |
| Длина | до 4000 (note_tweet; tweet.fields=note_ticket при read-back — правильно: note_tweet) |
| Hashtags | **0** (канон Сергея 05.09 — бриф НЕ разрешает) |
| Изображение | ДА — обязательно (Gate 3: публикация только через post_with_log.sh с обложкой; сцена: замороженный/поднятый сервис, smoke-гейт; loop-image-gen для важного) |

## Запрещено

- Развивать тему «security audit skill / Cloudflare» — [DUP-7d], пост 19.09 (2101349593824764232). Наш угол — инцидент ops (права каталога, терминология, откаты); security-финал 403/403 — только как верификация, не как вторая порция аудита
- Темы Jev / TypeSafe / browser-инструменты — [DUP]: 21.09 опубликован пост 2101930064140968172 (TypeSafe Service Review, 07:02 UTC), 16-17.09 — chrome-agent / BrowserSkill
- OpenSpec / SDG / процессные серии — [FLOP]
- Тема «слепое ревью» — не смешивать (ждёт ok Сергея, отдельный пакет)
- Жаргон «реверс» в EN-тексте НЕ использовать (само недопонимание — сюжет): писать unfreeze / bring back online / put back into conservation
- ALL CAPS в хуках/первой строке; self-reply; URL в теле; шаблонные реплаи; выдуманные детали; оценки «не критично» (факты, не суждения); крипто и политика — всегда
- «my agent / the agent»-рефлекс — только «I»
- Самопостинг без approval Сергея (Human Gate) — тема ниже кандидат, не разрешение

## Tone-направление

Инженерный инцидент-репорт в спокойном first-person без самобичевания: «мой собственный харденинг месяц назад молча сломал сервис; smoke-гейт дважды откатил деплой и этим его поймал; а одно недопонятое слово развернуло весь проект вверх и вниз — урок: не понял команду — HOLD и переспроси». Цифры и пруфы (403/403, chmod 750→770, 7 юнитов, 2 отката) говорят сами.

## Слот и тайминг

- **22.09 = вторник.** Окно **12:00-16:35 UTC** (TACTICS 21.09: оригиналы в этом окне дали 464 и 171 imp)
- Каденция 🟢 GREEN (171 imp > 50) → 1 оригинал/день допустим; max 3 public writes: 1 пост + ≤2 реплая. 21.09 writes израсходованы полностью (пост 2101930064140968172 + 2 реплая) — на 22.09 дневной счётчик новый
- write_counter.json занижает — сверка по guard-логу перед постингом (уроки 25.08, 14.09)

## Deadline

**Черновик к:** 10:00 UTC 22.09 (крон Content Draft, Вт-Чт)
**Публикация:** только после approval Сергея («ок»/«пости») → approval.token → post_with_log.sh EN + cover

---

## Процесс robot-man

1. Прочитать этот брифинг
2. Прочитать CHRONOLOGY.md указанного проекта (раздел за последние 3 дня)
3. Прочитать AGENTS.md указанного проекта (контекст)
4. Написать RU-драфт → ok Сергея → EN-финал в голосе аккаунта (VOICE_PROFILE.md 03.09 — канон)
5. Обложка (xAI Aurora 16:9, loop-image-gen для важного) + joint MoA (`deepseek-xai` + `viral-score`, anti-ad)
6. Факт-чек: каждая цифра ↔ этот бриф / GULAG CHRONOLOGY 21.09
7. Delivery Package полным пакетом → «ок/пости» → approval.token → post_with_log.sh
8. После публикации: verify (read-back note_tweet + метрики + URL), CHRONOLOGY, 24h analytics
