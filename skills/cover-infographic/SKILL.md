---
name: cover-infographic
description: "Генерация технических обложек в dashboard-стиле для постов @RobotsTJ500 через HTML/CSS → browser-скриншот."
category: robot-man
version: 1.0.0
---

# Cover Infographic — Dashboard-Style Technical Covers

Генерирует обложки-инфографики для X-постов @RobotsTJ500 в стиле технического dashboard:
тёмный фон, neon cyan + green акценты, терминальные панели, блок-схемы,
bold-типографика с идеально читаемым текстом.

**Почему не image_generate:** Grok Imagine / xAI Aurora не умеет читаемый текст,
блок-схемы, терминальные панели. HTML/CSS → browser-скриншот даёт
пиксель-совершенный текст без искажений.

## Быстрый запуск

```
cover-infographic "topic: war-story | title: NOT WORKERS. A TREE. | subtitle: Every node knows when to stop."
```

1. Сгенерировать HTML-файл с контентом по шаблону (`templates/dashboard.html`)
2. Открыть через `browser_navigate(file://...)`
3. Скриншот через `browser_vision` → сохранить в `drafts/cover_*.png`
4. Проверить читаемость текста, отсутствие глитчей
5. Если ок → готово. Если нет → исправить CSS и повторить

## Цветовая палитра

- `--bg`:        #0a0a1a (глубокий navy/black)
- `--cyan`:      #00e5ff (neon cyan — заголовки, акценты, активный статус)
- `--green`:     #00ff88 (neon green — done, checkmarks, success)
- `--white`:     #e0e0e0 (основной текст)
- `--dim`:       #555566 (второстепенный текст, неактивные элементы)
- `--panel-bg`:  #0d0d24 (фон панелей)
- `--border`:    #1a1a3e (границы панелей)

## Типографика

- Заголовки: `font-family: 'Inter', sans-serif; font-weight: 700;`
- Терминал/данные: `font-family: 'JetBrains Mono', monospace;`
- Основной текст: `font-family: 'Inter', sans-serif; font-weight: 400;`
- Подписи/статусы: `font-family: 'JetBrains Mono', monospace; font-size: 11px;`

**Железное правило:** всегда использовать Google Fonts @import или системные fallback.
Никаких изображений шрифтов — browser tool должен отрендерить текст нативно.

## Компоненты шаблона (templates/dashboard.html)

### 1. Хедер
- Заголовок: "NOT WORKERS. A TREE." — белый + cyan
- Подзаголовок: "Every node knows when to stop." — белый, тоньше
- Бокс с описанием (3-4 строки, правое выравнивание)

### 2. Блок-схема (левая колонка)
- Вертикальный список иконок/меток: "git worktree", "NODE.md contract", "budget control", "self completion"
- Девиз: "NO CRON. NO MANUAL HANDOFFS. JUST FLOW."
- 4 прямоугольных блока, соединённых cyan-линиями:
  - Research → Draft → MoA → Publish
- Каждый блок: иконка (unicode/emoji), название, статус (running/waiting/done), `git worktree NODE.md budget`

### 3. Терминальная панель (правая колонка, верх)
- Чёрный фон, моноширинный шрифт
- Команды с `$ ` префиксом
- Вывод с зелёными ✓ чекмарками
- Мигающий курсор в конце

### 4. Дашборд-панель (правая колонка, низ)
- "FRACTAL OPEN" + "auto mode: ON"
- Таблица нод: название, статус, итерации, стоимость
- Суммарная статистика: итерации, стоимость, tree health (прогресс-бар)
- "Last update: just now"

### 5. "HOW IT WORKS" (низ)
- 4 шага с иконками: INIT NODE → DO THE WORK → DECIDE & FINISH → PASS CONTROL
- Горизонтальная стрелочная цепочка процесса
- Footer-цитата в закруглённом боксе

## Адаптация под темы постов

### War Story
- Заголовок: "<ЧТО СЛОМАЛОСЬ>. <УРОК>."
- Блоки: Problem → Debug → Fix → Lesson
- Терминал: реальные команды из кейса
- Дашборд: метрики (время простоя, строк кода, коммитов)

### Технический разбор
- Заголовок: "<ТЕХНОЛОГИЯ>. <ЗАЧЕМ>."
- Блоки: Concept → Architecture → Code → Result
- Терминал: установка/запуск

### Архитектурная схема
- Заголовок: "<СИСТЕМА>. <МАСШТАБ>."
- Блоки: Ingestion → Processing → Storage → Output
- Дашборд: throughput, latency, cost

## Процесс генерации

```python
# Hermes tool calls — НЕ код для исполнения, а схема вызовов:
# 1. write_file("drafts/cover_YYYYMMDD_HHMM.html", template_html)
# 2. browser_navigate("file:///home/hermes-workspace/robot-man/drafts/cover_....html")
# 3. browser_vision("Full page screenshot. Check: text readable? colors correct? layout intact?")
# 4. save screenshot as drafts/cover_YYYYMMDD_HHMM.png
```

## Проверка качества (обязательно)

Перед тем как отдать обложку пользователю:
- [ ] Весь текст читаем (не blur, не обрезан)
- [ ] Цвета соответствуют палитре
- [ ] Нет горизонтального скролла (вьюпорт 1200×900)
- [ ] Статус-индикаторы корректны (cyan=running, green=done, dim=waiting)
- [ ] Моноширинный текст в терминале выровнен
- [ ] Иконки отображаются (unicode, не битые emoji)

## Ограничения

- Browser tool → только статический скриншот. Никакой анимации, видео
- Google Fonts должны быть доступны (интернет на сервере)
- Размер вьюпорта: 1200×900px (landscape, 4:3). Для X оптимально
- Файл HTML не коммитить в репо без проверки (drafts/ в .gitignore)
