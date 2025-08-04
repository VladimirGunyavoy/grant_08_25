# Makefile для компиляции презентации AIDA-T

# Основной файл презентации
MAIN = presentation_aida_t
TEX_FILES = $(MAIN).tex
PDF_FILES = $(MAIN).pdf

# Компилятор LaTeX
LATEX = pdflatex
BIBTEX = bibtex

# Флаги для компилятора
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# Директории
SLIDES_DIR = slides
BUILD_DIR = build

# Основная цель
all: $(PDF_FILES)

# Правило для компиляции PDF
$(MAIN).pdf: $(MAIN).tex $(wildcard $(SLIDES_DIR)/*.tex)
	@echo "Компиляция презентации AIDA-T..."
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	@echo "Презентация успешно скомпилирована: $(MAIN).pdf"

# Создание директорий
dirs:
	@mkdir -p $(SLIDES_DIR)
	@mkdir -p $(BUILD_DIR)

# Очистка временных файлов
clean:
	@echo "Очистка временных файлов..."
	@rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.fls *.fdb_latexmk *.synctex.gz
	@echo "Временные файлы удалены"

# Полная очистка включая PDF
distclean: clean
	@echo "Удаление PDF файлов..."
	@rm -f $(PDF_FILES)
	@echo "Все файлы удалены"

# Быстрая компиляция для отладки
quick: $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex

# Просмотр PDF (для Linux/macOS)
view: $(PDF_FILES)
	@if command -v evince >/dev/null 2>&1; then \
		evince $(MAIN).pdf & \
	elif command -v open >/dev/null 2>&1; then \
		open $(MAIN).pdf; \
	else \
		echo "Установите evince или используйте свой PDF-просмотрщик"; \
	fi

# Справка
help:
	@echo "Доступные команды:"
	@echo "  all      - Компиляция презентации"
	@echo "  quick    - Быстрая компиляция (без повтора)"
	@echo "  clean    - Удаление временных файлов"
	@echo "  distclean- Полная очистка"
	@echo "  view     - Открыть PDF"
	@echo "  dirs     - Создать необходимые директории"
	@echo "  help     - Показать эту справку"

.PHONY: all clean distclean quick view dirs help