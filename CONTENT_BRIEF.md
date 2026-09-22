# CONTENT_BRIEF — LCM rollout (активный, 2026-09-22; источник: CONTENT_BRIEF_LCM.md 21.09)

**Автор:** Hermes (default) — стратег
**Получатель:** robot-man
**Цель:** один пост для @RobotsTJ500. Публикация одобрена владельцем 22.09 («пости»).

## Факты (только эти, п.1–19 CONTENT_BRIEF_LCM.md)

| # | Факт |
|---|------|
| 1 | hermes-lcm v1.0.0-rc.1, пин 8d1b1e6d |
| 2 | SQLite lcm.db + FTS, DAG-саммари, 15 recall-тулов |
| 3 | Пилот с 19.09, forced-recall тест 20.09 прошёл |
| 4 | Флот 9 профилей |
| 5 | Бэкапы config.yaml.pre-lcm-20260921 |
| 6 | Сканер DANGEROUS: 87 findings, 1 critical embedded_private_key |
| 7 | Клон-анализ: ложное срабатывание, синтетический PEM в стресс-тесте, реальных секретов 0 |
| 8 | Разовый обход скана + issue апстриму |
| 9 | Issue stephenschoettler/hermes-lcm#616 OPEN |
| 10 | plugins doctor OK, 0 fail |
| 11 | context.engine compressor → lcm |
| 12 | Verify: doctor healthy 16/16, 0 warnings; 15/15 тулов; 87 сообщений; 11.3% vs 32% |
| 13 | One-shot recall-тест 22.09 16:19 UTC |
| 14 | 6 из 8 профилей из глобального каталога |
| 15 | 2 профиля локальный discovery — индивидуально |
| 16 | Секрет-хук блокирует inline-env — wrapper-скрипт |
| 17 | Sweep 9/9 verified |
| 18 | Rollback-якоря в каждом профиле |
| 19 | Тест-фикстуры с фейковыми ключами легитимны; сканер контекстно-слеп |

Дополнительно разрешено (из отчёта директора 22.09): свежий хвост 32 сообщения, глубина DAG 3, FTS-индекс, lcm_doctor покрывает schema/FTS/WAL/осиротевшие узлы/lineage, проверка точной формулировки только через recall.

## Формат и голос

| Параметр | Значение |
|----------|----------|
| Тип поста | War Story / Tech Breakdown |
| Аккаунт | @RobotsTJ500 |
| Голос | EN first-person «I», «Building in public. 🤖», hashtags 0, без URL |
| Mentions | @SteveSchoettler, @witcheer |
| Изображение | /home/hermes-workspace/robot-man/drafts/lcm_cover_v2.png |
| Длина | до 4000 (note_tweet) |

## Запрещено

- Цифры вне таблицы; ALL CAPS; self-reply; URL в теле; «my agent»; крипто/политика
- Обход сканера без деталей флагов, не как «хак»; security-audit-угол не развивать
- Публикация без approval.token

## Механика публикации

`echo "$(uuidgen)" > data/approval.token && bash post_with_log.sh "$(cat drafts/lcm-rollout_v1_en.txt)" /home/hermes-workspace/robot-man/drafts/lcm_cover_v2.png`
После: read-back note_tweet, published_posts.jsonl, CHRONOLOGY, 24h analytics.
