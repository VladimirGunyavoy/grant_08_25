# AIDA Grant Project Repository

Репозиторий проекта AIDA для грантовых заявок и научных публикаций.

## 📁 Структура проекта

```
grant_08_25/
├── README.md                    # Этот файл
├── scripts/                     # Python скрипты
│   ├── scrape_dois_ajax.py      # Скрипт для извлечения статей из Google Scholar
│   ├── json_to_bibtex_enhanced.py # Генерация BibTeX из JSON данных
│   ├── analyze_publications.py  # Анализ публикаций и статистика
│   ├── add_citations.py         # Добавление цитирований в LaTeX
│   └── ...                      # Другие вспомогательные скрипты
├── data/                        # Данные и промежуточные файлы
│   ├── found_dois_ajax.json     # Извлеченные данные статей
│   ├── articles_metadata.json   # Метаданные статей
│   ├── publication_stats.json   # Статистика публикаций
│   └── ...                      # Другие JSON и текстовые файлы
├── documents/                   # Документы проекта
│   ├── technical_description.md # Техническое описание
│   ├── аннотация_проекта.md     # Аннотация проекта
│   ├── краткое_описание_продукта.md # Описание продукта
│   ├── answers.md               # Ответы на вопросы
│   ├── final_answers.md         # Финальные ответы
│   └── ...                      # PDF и DOCX документы
├── presentations/               # Презентации и визуализации
│   ├── структура_доходов_AIDA-T.png # Диаграмма доходов
│   ├── структура_доходов_диаграмма.html # Интерактивная диаграмма
│   └── ...                      # Другие изображения и HTML файлы
├── central uni grant/           # Основные грантовые документы
│   ├── my_bib.bib              # BibTeX база данных публикаций
│   ├── Osinenko_list_of_papers_no_preprints.tex # LaTeX документ со списком публикаций
│   ├── Osinenko_list_of_papers_no_preprints.pdf # Скомпилированный PDF
│   └── ...                     # Другие грантовые документы
├── aida_t_presentation/         # Презентация проекта AIDA
├── privproject2022-agrobot/     # Документы по проекту агробота
├── Разделы/                     # Разделы грантовой заявки
└── не хватает данных/           # Документы для доработки
```

## 🎯 Основные компоненты

### 📊 Анализ публикаций
- **Скрипты**: `scripts/analyze_publications.py`, `scripts/add_citations.py`
- **Данные**: `data/found_dois_ajax.json`, `data/publication_stats.json`
- **Результат**: `central uni grant/Osinenko_list_of_papers_no_preprints.pdf`

### 🔍 Извлечение данных
- **Скрипт**: `scripts/scrape_dois_ajax.py`
- **Источник**: Google Scholar профиль П.В. Осиненко
- **Результат**: 44 уникальные публикации с полными метаданными

### 📈 Статистика публикаций
- **Всего статей**: 44
- **Период**: 2014-2025
- **Публикаций первым автором**: 26
- **Цитирования**: 512 (общее), 428 (с 2020)
- **h-индекс**: 11
- **i10-индекс**: 14/12

## 🚀 Быстрый старт

### 🎯 **VS Code (Рекомендуется)**
1. Откройте проект в VS Code
2. Установите рекомендуемые расширения (появится уведомление)
3. Используйте команды:
   - **Ctrl+Shift+P** → "Tasks: Run Task" → выберите нужную задачу
   - **Ctrl+Shift+P** → "LaTeX Workshop: Build LaTeX project" (для LaTeX файлов)
   - **F5** → для запуска Python скриптов

### 📋 **Доступные задачи VS Code:**
- **Compile LaTeX Document** - компиляция LaTeX с автоматической очисткой
- **Generate BibTeX** - генерация BibTeX из JSON данных
- **Analyze Publications** - анализ публикаций и статистика
- **Full Build (All Steps)** - полный процесс (анализ + генерация + компиляция)
- **Clean Temporary Files** - очистка временных файлов

### 💻 **Командная строка:**
```bash
# Установка зависимостей
make install

# Полный процесс
make all

# Только компиляция LaTeX
make latex

# Только генерация BibTeX
make bibtex
```

## 📋 Требования

- Python 3.7+
- LaTeX (pdflatex, bibtex)
- Библиотеки Python: requests, beautifulsoup4, json

## 🔧 Установка зависимостей

```bash
pip install requests beautifulsoup4
```

## 📝 Примечания

- Все скрипты протестированы и готовы к использованию
- BibTeX файл содержит 44 уникальные публикации без дубликатов
- LaTeX документ включает статистику и визуализацию цитирований
- Данные актуальны на момент создания (2025)

## 📞 Контакты

Для вопросов по проекту обращайтесь к команде AIDA.
