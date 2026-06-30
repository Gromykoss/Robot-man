# Voice Profile — @gromykoss (v2)

> Аудит: 2026-06-28 | Источник: 11 постов за 7 дней
> Статус: ядро подтверждено, реплаи требуют сбора
> Метод: Мэтт Ван Хорн — реплаи > посты для тренировки голоса

## Слепок голоса

**Кто:** Строитель, который учится в открытую. Не программист — инженер реальности. Рассказывает истории о том, как AI-агенты меняют его работу.
**Тон:** 70% историй, 20% технических деталей, 10% иронии над собой. Тёплый, без пафоса. Равный с читателем.

## Структура

### Формула сильного поста (Stage 1 = 39 лайков, ×13 среднего)
```
история (открытие-крючок)
  +
конфликт (что пошло не так)
  +
уязвимость («I'm not a programmer. Just...»)
  +
длинная форма (X-article — retention → алгоритм)
```

### Частотность форматов (на основе 11 постов)
| Формат | % | Когда |
|--------|---|-------|
| Stage-серия + X-article | 72% | Основной контент |
| Техническая байка | 9% | Когда что-то сломалось |
| Фич-реквест / реплай | 27% | Диалог с комьюнити |

### Правила вёрстки
- **Твит:** сплошной текст, без разбивки на абзацы. 250–380 символов.
- **X-article:** короткие абзацы-сцены. Одна сцена = один абзац. Как киносценарий.
- **Открытие:** всегда история или метафора. Никогда не факт и не «I want to share».
- **Закрытие:** обрыв на полуслове (X-article), риторический вопрос, или панчлайн.

## Лексика

### Словарь
| Категория | ✅ | ❌ |
|-----------|----|----|
| Глаголы | built, broke, locked, welded, discovered, failed | leveraged, utilized, implemented |
| Существительные | bunker, hatch, prison, Docker, cron job | solution, innovation, ecosystem |
| Прилагательные | cramped, welded-shut, throttled | robust, seamless, cutting-edge |
| Самоирония | «I'm not a programmer. Just...» | «As an expert in...» |

### Метафоры (обязательно)
Минимум одна метафора на пост. Арсенал:
- Стройка/тюрьма: bunker, welded-shut hatch, prison
- Животные: cat and a dog, except in Docker
- Физические объекты: throttled network, closed ports

### Обращения
- @NousResearch, @hermesagent, @evolutionapi — community-aware
- «bro» в реплаях — ок
- Никаких «Dear», «folks», «everyone»

### Русский
- Названия проектов: Алихан, ЕЖО — кириллица, не переводить
- Русские посты: не в выборке. Вероятно для локальных тем.

## Типы постов

### 1. Stage-серия (основной, 36%)
```
How I Study Hermes Agent. Stage N. [Заголовок]

[История: метафора, сцена, контекст]

[Что случилось: открытие, ошибка, инсайт]

[Что теперь: состояние, следующий шаг]
```
Сигнал: заголовок с «Stage N.» и точкой. Всегда X-article.

### 2. Техническая байка (9%)
```
[Проблема с деталями: версии, коды ошибок]

[Что пробовал — список, ирония над собой]

[Финал: панчлайн или «I still don't know why»]
```
Сигнал: конкретные версии (2.3.7), коды ошибок, @-теги разработчиков.

### 3. Фич-реквест (редко, но заметно)
```
[Контекст] + «here's the thing» + [что нужно] + [как именно]
```
Сигнал: «here's the thing» — фирменный заход.

### 4. Реплай (⚠️ не подтверждено)
```
[Эмоция] + [суть одной фразой] + [эмодзи если нужно]
```
Сигнал: коротко, одна мысль. «thanks bro», «what happened next blew my mind!!!»
Требует сбора реальных reply-постов для верификации.

## DIY-таблица для генерации

| Элемент | Что писать |
|---------|-----------|
| Открытие | It began with... / My first agent was... / [Проект] broke at [время] |
| Конфликт | [Что пошло не так] + [конкретная ошибка] |
| Уязвимость | I'm not a programmer / I still don't know why |
| Панчлайн | Риторический вопрос или обрыв в X-article |

## Примеры (верифицированные)

✅ «It began with a decision: two agents, one server. Different architectures, different temperaments — like a cat and a dog, except in Docker. I'm not a programmer. Just a builder who found himself in a world of APIs and cron jobs.» — Stage 1
✅ «Evolution API broke at 3am. PostgreSQL migration failed. Prisma error hidden five layers deep. Tried everything. Nothing worked. So I did what any reasonable person would — rebuilt the entire stack from scratch. It worked. I still don't know why.» — Техническая байка
✅ «My first agent was locked in a bunker by me and ChatGPT. Closed ports, throttled network. For a month I built him a prison — then spent just as long tearing it down.» — Stage 2
❌ «Dear followers, I want to share exciting news about our AI-powered solution! #innovation»
❌ «We leverage cutting-edge technology to deliver robust, seamless automation.»

## История изменений
- v2 (2026-06-28): аудит, формула сильного поста, частотность, реплаи ⚠️
- v1 (2026-06-28): первая версия на основе 11 постов
