# CONTENT_BRIEF — 2026-09-18

**Автор:** Hermes (default) — стратег. Ночная генерация 2026-09-17 23:40 UTC (крон Content Brief).
**Rev:** полная перезапись. Предыдущий бриф (BrowserSkill, rev.2 от 17.09) — тема опубликована robot-man сегодня 12:37 UTC (пост 2100564709170729308, 290 imp / 3❤ / 5💬), факты израсходованы.

**Получатель:** robot-man (профиль) — голос/исполнитель
**Цель:** один пост для @RobotsTJ500

---

## ШАГ 0.5 — Engagement Feedback (TACTICS.md от 17.09 05:27, свежий)

TOP-3 за 7 дней (на закрытие 17.09):
- BrowserSkill (17.09, 12:37) → 290 imp / 3❤ / 5💬 / 1 quote → вывод: свежий инструмент + «works with any agent that can run a shell» = лучшая дистрибуция недели
- Chrome-agent Service Review (16.09) → 66 imp / 2❤ / 1💬 (~20ч) → верифицированные цифры-скрин (200000 доменов) дают живой тред
- Harden AIF (14.09) → 98 imp / 1❤ / 3💬 → 3 входящих reply — ветка живёт за счёт ответов

FLOP-3:
- Reply SurgeOnHeff (14.09) → 22 imp / 1❤ → ответ-в-тред работает слабее оригинала
- Post Part 3 (08.09) → 35 imp / 1❤ → замыленный формат OpenSpec-серии [DUP-7d]
- Nightly reply 20995114 (14.09) → 1❤ / 0💬 → реплай-марафон не окупается

**Использование:** работающие форматы — свежий внешний инструмент с цифрами и границей применимости, верифицированная цифра-скрин, пост с последующей живой веткой reply. Эти качества включены в выбранную тему ниже. FLOP-сигнал: OpenSpec/SDG-процессные серии — не повторять.

---

## Тема

**«Я поставил прод на паузу вместо того, чтобы его убить — и вот что для этого понадобилось»** — консервация GULAG: заморозка живого production-мессенджера с 11 пользователями, чтобы освободить сервер, сохранив полный реверс по одной команде.

---

## Факты (верифицированы по CHRONOLOGY GULAG)

| # | Факт | Источник |
|---|------|----------|
| 1 | Консервация выполнена 13.09.2026 по команде Сергея: освободить сервер 89.169.180.244 для другого проекта, сохранив доступ и возможность полного реверса по команде | CHRONOLOGY GULAG, раздел 2026-09-13 |
| 2 | Причина консервации: 11 активных пользователей, 0 новых анкет 48 дней — продукт жив, но рост нулевой | CHRONOLOGY GULAG: «11 активных пользователей (deactivated=0)», «46-й день без новых анкет» (11.09) |
| 3 | Снапшот VPS: консистентная БД sqlite .backup 222M + configs tar.gz 101M (579 файлов) + system-manifest; секреты → AES256-gpg бандл (decrypt-test 27 объектов OK); SHA256 в MANIFEST-SHA256.txt | CHRONOLOGY GULAG 13.09, п.2 |
| 4 | Freeze-процедура: smoke 12/12 PRE ✓ → stop+disable 7 systemd-юнитов (receiver, notify, okhrana, matrix-synapse, nginx, coturn, livekit); RAM 638→470Mi; порты 8008/5000/443/7880 освобождены | CHRONOLOGY GULAG 13.09, п.5 |
| 5 | Верификация после стопа: POST-FREEZE systemctl is-active ×7 = inactive, ps — нет процессов, ss — порты свободны | CHRONOLOGY GULAG «Как проверено» |
| 6 | Freeze + git tag `freeze/pre-conservation-20260913` + freeze.meta (git_sha 1d0e7bd3) — откат через deploy.sh --freeze | CHRONOLOGY GULAG, п.3 |
| 7 | CDD-документация в репо: CONSERVATION.md + 7-уровневая спека (инфраструктура → Synapse → сервисы → приложение → репо → зависимости → точки реверса) + RESTORE-RUNBOOK.md с 3 сценариями (A пробуждение, B пересборка на новом сервере, C частичный реверс) | CHRONOLOGY GULAG, п.4 |
| 8 | Offsite restic-бэкап 03:00 в Yandex Object Storage оставлен ЖИВЫМ — бэкапы замороженного прода продолжаются | CHRONOLOGY GULAG, п.5 |
| 9 | Мониторы Hermes (Health Check, nginx guard, CHRONOLOGY+брифинг) поставлены на паузу, read-only мониторы остались живыми; resume при реверсе | CHRONOLOGY GULAG, п.6 |
| 10 | Коммит консервации `675c7354` 13.09 03:42 UTC + CI-whitelist доков `e136e0f4` + карта сборки `bd58eca2` | git log GULAG (CHRONOLOGY) |

## Контекст проекта

**Проект:** GULAG (тюремный мессенджер) — консервация инфраструктуры
**CHRONOLOGY:** `/home/hermes-workspace/gooolag/CHRONOLOGY.md` (раздел 2026-09-13)
**AGENTS.md:** `/home/hermes-workspace/gooolag/AGENTS.md`
**Репо-доки:** CONSERVATION.md, conservation/CDD-GULAG-conservation.md, conservation/RESTORE-RUNBOOK.md

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story / engineering post |
| Аккаунт | @RobotsTJ500 |
| Голос | English first-person «I» — технический, прямой, без пафоса (VOICE_PROFILE.md) |
| Длина | до 4000 знаков (note_tweet) |
| Hashtags | 0 (канон Сергея 05.09) |
| Изображение | обложка через loop, цель 8-10/10 (тема визуальная: замороженный сервер, иней на стойке) |
| Closing | «Building in public. 🤖» |

## Запрещено

- ALL CAPS в хуках (всегда)
- Self-reply (всегда)
- URL в теле поста (всегда)
- Выдуманные детали (всегда) — каждая цифра из таблицы фактов или CHRONOLOGY GULAG
- Попсовые хуки-клише («Most X lie…») — Сергей 16.09
- «не программист — строитель» — заезжено (15.08)
- «окно в будущее» — пошло (отвергнуто)
- Название проекта/заказчика и домен сервера НЕ раскрывать (приватность) — говорить «a production messenger», «the server»

## Tone-направление

Спокойная инженерная история с иронией про «агент, который хоронит свой прод так бережно, что тот можно разбудить одной командой»: цифры (222M, 579 файлов, 7 юнитов, RAM 638→470), сцена (smoke 12/12 перед стопом, все юниты inactive, порты свободны), урок (консервация ≠ удаление: freeze-tag + gpg-секреты + живой offsite-бэкап = обратимый сон вместо необратимой смерти).

## Deadline

**Черновик к:** 2026-09-18 12:00 UTC (Content Gate окно 15-16 UTC)
**Публикация:** после approval Сергея («ок» → токен → post_with_log.sh с обложкой)

---

## Процесс robot-man

1. Прочитать этот бриф
2. Прочитать CHRONOLOGY.md GULAG (раздел 2026-09-13)
3. Прочитать AGENTS.md GULAG (контекст)
4. RU-драфт (VOICE_PROFILE.md + ENGINEERING_POST_TEMPLATE.md) → `drafts/gulag_conservation_v1_ru.md`
5. MoA: deepseek-xai + viral-score, оба agree → пост
6. Факт-чек: сверить каждую цифру с таблицей фактов брифа
7. Обложка через loop, 8-10/10
8. RU → ok Сергея → EN-финал + обложка → Delivery Package
9. После «пости» → токен → `bash post_with_log.sh "EN text" /abs/path/cover.png`
10. CHRONOLOGY.md robot-man + published_posts.jsonl

---

## Scoring (внутренний, для отчётности)

| Источник | Score | Итог |
|----------|-------|------|
| GULAG консервация (13.09) | 33/42 | **Победитель → BRIEF** |
| ACCOUNT_ID-баг robot-man (17.09, BUGS.md) | 26/42 | Проиграл: дуга без фикс-развязки, разнообразие (robot-man был источником вчера) |
| Alikhan SDG-lockdown (12-14.09) | 26/42 | Проиграл: свежесть >48ч, процессная специфика |
| RAB9 burnie-tracker (17.09) | VETO | Крипто-контент (цены токенов) — мгновенный disqualify |
| vault-эволюция (3 дня) | — | Пусто: коммитов в SOUL/OPERATIONS/scorecard/Engineering Loop за 3 дня нет |
| TACTICS «слепое ревью» | — | Не бриффю: RU-драфт уже у Human Gate с 15.09 (зона Content Gate) |
| TACTICS SAM follow-up | — | Прямо запрещено запускать без ok Сергея (handoff) |

**Anti-dup:** `operators/published_topic_check.py` — «консервация conservation server freeze» exit 0, «wrong account ID hardcoded analytics» exit 0, «BrowserSkill» exit 0 (последний — мёртв, тема опубликована).
