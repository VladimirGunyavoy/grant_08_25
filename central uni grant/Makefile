# Makefile для компиляции LaTeX документа AIDA-T

# Основные переменные
TARGET = Описание_результатов_исследований
LATEX = pdflatex
BIBTEX = bibtex
CLEAN_EXTENSIONS = aux log out toc lot lof blg bbl bcf run.xml fdb_latexmk fls synctex.gz

# Цвета для вывода
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[1;33m
NC = \033[0m # No Color

# Основная цель
all: $(TARGET).pdf

# Компиляция PDF
$(TARGET).pdf: $(TARGET).tex
	@echo "$(GREEN)Компиляция LaTeX документа...$(NC)"
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	@echo "$(GREEN)Документ успешно скомпилирован!$(NC)"

# Компиляция с библиографией (если понадобится)
bib: $(TARGET).tex
	@echo "$(YELLOW)Компиляция с библиографией...$(NC)"
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	$(BIBTEX) $(TARGET)
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	@echo "$(GREEN)Документ с библиографией готов!$(NC)"

# Быстрая компиляция (однократная)
quick: $(TARGET).tex
	@echo "$(YELLOW)Быстрая компиляция...$(NC)"
	$(LATEX) -interaction=nonstopmode $(TARGET).tex
	@echo "$(GREEN)Готово!$(NC)"

# Очистка временных файлов
clean:
	@echo "$(YELLOW)Очистка временных файлов...$(NC)"
	rm -f $(addprefix $(TARGET)., $(CLEAN_EXTENSIONS))
	@echo "$(GREEN)Временные файлы удалены!$(NC)"

# Полная очистка (включая PDF)
cleanall: clean
	@echo "$(YELLOW)Удаление PDF файла...$(NC)"
	rm -f $(TARGET).pdf
	@echo "$(GREEN)Все файлы удалены!$(NC)"

# Просмотр PDF (для Linux/Mac)
view: $(TARGET).pdf
	@echo "$(GREEN)Открытие PDF...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(TARGET).pdf; \
	elif command -v open > /dev/null; then \
		open $(TARGET).pdf; \
	else \
		echo "$(RED)Не удалось открыть PDF автоматически$(NC)"; \
	fi

# Компиляция и просмотр
viewall: all view

# Проверка зависимостей
check:
	@echo "$(YELLOW)Проверка зависимостей...$(NC)"
	@if ! command -v $(LATEX) > /dev/null; then \
		echo "$(RED)Ошибка: $(LATEX) не установлен$(NC)"; \
		echo "Установите TeX Live или MiKTeX"; \
		exit 1; \
	fi
	@echo "$(GREEN)Все зависимости установлены!$(NC)"

# Помощь
help:
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo "  all      - Полная компиляция документа (2 прохода)"
	@echo "  quick    - Быстрая компиляция (1 проход)"
	@echo "  bib      - Компиляция с библиографией"
	@echo "  clean    - Удаление временных файлов"
	@echo "  cleanall - Полная очистка (включая PDF)"
	@echo "  view     - Открытие PDF в браузере"
	@echo "  viewall  - Компиляция и открытие PDF"
	@echo "  check    - Проверка зависимостей"
	@echo "  help     - Показать эту справку"

# Установка зависимостей (для Ubuntu/Debian)
install-deps:
	@echo "$(YELLOW)Установка зависимостей для Ubuntu/Debian...$(NC)"
	sudo apt-get update
	sudo apt-get install -y texlive-full texlive-lang-russian
	@echo "$(GREEN)Зависимости установлены!$(NC)"

# Установка зависимостей (для macOS)
install-deps-mac:
	@echo "$(YELLOW)Установка зависимостей для macOS...$(NC)"
	@if command -v brew > /dev/null; then \
		brew install --cask mactex; \
	else \
		echo "$(RED)Homebrew не установлен. Установите его с https://brew.sh$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Зависимости установлены!$(NC)"

.PHONY: all bib quick clean cleanall view viewall check help install-deps install-deps-mac
