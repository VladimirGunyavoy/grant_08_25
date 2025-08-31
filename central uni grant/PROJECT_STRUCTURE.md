# Предложения по улучшению структуры проекта AIDA-T

## Текущие проблемы структуры

1. **Дублирование файлов** - одинаковые файлы в разных папках
2. **Нелогичная иерархия** - файлы разбросаны по разным уровням
3. **Отсутствие четкого разделения** между исходниками, документацией и результатами
4. **Смешение форматов** - LaTeX, Markdown, PDF в одной папке

## Предлагаемая новая структура

```
central-uni-grant/
├── 📁 docs/                          # Документация проекта
│   ├── 📄 README.md                  # Основное описание проекта
│   ├── 📄 CONTRIBUTING.md            # Правила участия
│   ├── 📄 CHANGELOG.md               # История изменений
│   ├── 📄 STATUS.md                  # Статус проекта
│   └── 📄 SUMMARY.md                 # Краткое резюме
│
├── 📁 applications/                   # Заявки и документы
│   ├── 📁 central-uni/               # Заявка в центральный университет
│   │   ├── 📄 main.tex              # Основной LaTeX файл
│   │   ├── 📄 bibliography.bib       # Библиография
│   │   ├── 📁 assets/               # Изображения и ресурсы
│   │   ├── 📁 sections/             # Разделы документа
│   │   └── 📄 Makefile              # Скрипт компиляции
│   │
│   ├── 📁 start-ii/                  # Заявка СТАРТ-ИИ
│   └── 📁 other/                     # Другие заявки
│
├── 📁 research/                       # Исследовательские материалы
│   ├── 📁 publications/              # Публикации
│   │   ├── 📄 bibliography.bib       # Общая библиография
│   │   ├── 📁 papers/               # PDF статей
│   │   └── 📄 citations.md          # Список цитирований
│   │
│   ├── 📁 technical/                 # Техническая документация
│   │   ├── 📄 technical_description.md
│   │   ├── 📄 project_requirements.md
│   │   └── 📁 diagrams/             # Диаграммы и схемы
│   │
│   └── 📁 data/                      # Данные и результаты
│       ├── 📄 publication_stats.json
│       └── 📁 datasets/             # Датасеты
│
├── 📁 scripts/                        # Скрипты и утилиты
│   ├── 📄 build.sh                   # Скрипт сборки
│   ├── 📄 analyze_publications.py    # Анализ публикаций
│   └── 📄 convert_bib.py            # Конвертация библиографии
│
├── 📁 presentations/                  # Презентации
│   ├── 📁 aida-t/                   # Презентация AIDA-T
│   └── 📁 general/                   # Общие презентации
│
├── 📁 legal/                          # Юридические документы
│   ├── 📁 ooo/                       # Документы ООО
│   └── 📁 residency/                 # Документы резиденства
│
├── 📁 config/                         # Конфигурационные файлы
│   ├── 📄 .gitignore
│   ├── 📄 .editorconfig
│   └── 📄 vscode-settings.json
│
└── 📁 output/                         # Результаты компиляции
    ├── 📁 pdf/                       # PDF файлы
    └── 📁 temp/                      # Временные файлы
```

## Преимущества новой структуры

### 1. **Логическое разделение**
- `docs/` - вся документация проекта
- `applications/` - заявки по типам
- `research/` - исследовательские материалы
- `scripts/` - автоматизация

### 2. **Устранение дублирования**
- Один основной LaTeX файл
- Общая библиография
- Централизованные ресурсы

### 3. **Улучшенная навигация**
- Понятные названия папок
- Группировка по назначению
- Легкий поиск файлов

### 4. **Масштабируемость**
- Легко добавлять новые заявки
- Структура готова для роста
- Четкие правила организации

## План миграции

### Этап 1: Создание новой структуры
```bash
# Создать новые папки
mkdir -p docs applications/central-uni/{assets,sections} research/{publications,technical,data} scripts presentations legal config output/{pdf,temp}
```

### Этап 2: Перенос файлов
```bash
# Перенести основные файлы
mv README.md docs/
mv STATUS.md docs/
mv SUMMARY.md docs/

# Перенести LaTeX файлы
mv UI/application/latex/result_5pages.tex applications/central-uni/main.tex

# Перенести скрипты
mv scripts/* scripts/
```

### Этап 3: Обновление ссылок
- Обновить пути в Makefile
- Исправить ссылки в документах
- Обновить .gitignore

### Этап 4: Тестирование
- Проверить компиляцию
- Убедиться в работоспособности скриптов
- Проверить все ссылки

## Рекомендации по именованию

### Файлы
- Использовать snake_case для файлов
- Понятные, описательные имена
- Включать версию в имя при необходимости

### Папки
- Использовать kebab-case для папок
- Краткие, но понятные названия
- Группировать по функциональности

### Документы
- Добавить дату в имя для версий
- Использовать префиксы для типов (draft_, final_)
- Включать краткое описание в имя

## Автоматизация

### Makefile для новой структуры
```makefile
# Основные цели
all: clean compile view
compile: pdf/main.pdf
clean: clean-temp clean-pdf

# Компиляция
pdf/main.pdf: applications/central-uni/main.tex
	@echo "Компиляция LaTeX документа..."
	pdflatex -output-directory=output/pdf applications/central-uni/main.tex
	bibtex output/pdf/main
	pdflatex -output-directory=output/pdf applications/central-uni/main.tex
	pdflatex -output-directory=output/pdf applications/central-uni/main.tex

# Очистка
clean-temp:
	rm -rf output/temp/*

clean-pdf:
	rm -rf output/pdf/*.pdf
```

### Скрипт миграции
```bash
#!/bin/bash
# migrate_structure.sh

echo "Начинаем миграцию структуры проекта..."

# Создание новой структуры
mkdir -p docs applications/central-uni/{assets,sections} research/{publications,technical,data} scripts presentations legal config output/{pdf,temp}

# Перенос файлов
echo "Переносим файлы..."

# Документация
mv README.md docs/ 2>/dev/null || echo "README.md уже перемещен"
mv STATUS.md docs/ 2>/dev/null || echo "STATUS.md уже перемещен"
mv SUMMARY.md docs/ 2>/dev/null || echo "SUMMARY.md уже перемещен"

# LaTeX файлы
mv UI/application/latex/result_5pages.tex applications/central-uni/main.tex 2>/dev/null || echo "LaTeX файл уже перемещен"

echo "Миграция завершена!"
echo "Проверьте новую структуру в папке docs/STRUCTURE.md"
```

## Заключение

Новая структура обеспечит:
- ✅ Лучшую организацию файлов
- ✅ Устранение дублирования
- ✅ Упрощение навигации
- ✅ Масштабируемость проекта
- ✅ Стандартизацию именования

Рекомендуется внедрять изменения поэтапно, тестируя каждый шаг.
