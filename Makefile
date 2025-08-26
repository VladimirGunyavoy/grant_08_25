# AIDA Grant Project Makefile

.PHONY: help install clean analyze bibtex latex pdf all

# Основные команды
help:
	@echo "Доступные команды:"
	@echo "  install   - Установка зависимостей"
	@echo "  analyze   - Анализ публикаций"
	@echo "  bibtex    - Генерация BibTeX"
	@echo "  latex     - Компиляция LaTeX документа"
	@echo "  pdf       - Создание финального PDF"
	@echo "  clean     - Очистка временных файлов"
	@echo "  all       - Выполнить все шаги"

# Установка зависимостей
install:
	pip install -r requirements.txt

# Анализ публикаций
analyze:
	cd scripts && python3 analyze_publications.py

# Генерация BibTeX
bibtex:
	cd scripts && python3 json_to_bibtex_enhanced.py

# Компиляция LaTeX
latex:
	cd "central uni grant" && \
	pdflatex -interaction=nonstopmode Osinenko_list_of_papers_no_preprints.tex && \
	bibtex Osinenko_list_of_papers_no_preprints && \
	pdflatex -interaction=nonstopmode Osinenko_list_of_papers_no_preprints.tex && \
	pdflatex -interaction=nonstopmode Osinenko_list_of_papers_no_preprints.tex

# Создание PDF
pdf: bibtex latex

# Полный процесс
all: install analyze bibtex latex

# Очистка временных файлов
clean:
	find . -name "*.aux" -delete
	find . -name "*.log" -delete
	find . -name "*.out" -delete
	find . -name "*.bbl" -delete
	find . -name "*.blg" -delete
	find . -name "*.fdb_latexmk" -delete
	find . -name "*.fls" -delete
	find . -name "*.synctex.gz" -delete
	find . -name "*.toc" -delete
	find . -name "*.nav" -delete
	find . -name "*.snm" -delete
