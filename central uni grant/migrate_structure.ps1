# PowerShell скрипт для миграции структуры проекта AIDA-T
# Запуск: .\migrate_structure.ps1

Write-Host "🚀 Начинаем миграцию структуры проекта AIDA-T..." -ForegroundColor Green

# Функция для создания папки с проверкой
function Create-Directory {
    param([string]$Path)
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "✅ Создана папка: $Path" -ForegroundColor Cyan
    } else {
        Write-Host "ℹ️  Папка уже существует: $Path" -ForegroundColor Yellow
    }
}

# Функция для перемещения файла с проверкой
function Move-FileSafe {
    param([string]$Source, [string]$Destination)
    if (Test-Path $Source) {
        try {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "✅ Перемещен: $Source -> $Destination" -ForegroundColor Green
        } catch {
            Write-Host "❌ Ошибка при перемещении $Source : $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️  Файл не найден: $Source" -ForegroundColor Yellow
    }
}

Write-Host "📁 Создание новой структуры папок..." -ForegroundColor Blue

# Создание основной структуры
$folders = @(
    "docs",
    "applications\central-uni\assets",
    "applications\central-uni\sections", 
    "applications\start-ii",
    "applications\other",
    "research\publications\papers",
    "research\technical\diagrams",
    "research\data\datasets",
    "scripts",
    "presentations\aida-t",
    "presentations\general",
    "legal\ooo",
    "legal\residency",
    "config",
    "output\pdf",
    "output\temp"
)

foreach ($folder in $folders) {
    Create-Directory $folder
}

Write-Host "📄 Перемещение файлов..." -ForegroundColor Blue

# Перемещение документации
$docsFiles = @{
    "README.md" = "docs\README.md"
    "STATUS.md" = "docs\STATUS.md"
    "SUMMARY.md" = "docs\SUMMARY.md"
    "INSTALL.md" = "docs\INSTALL.md"
    "PERL_FIX.md" = "docs\PERL_FIX.md"
    "Описание_результатов_исследований.md" = "docs\Описание_результатов_исследований.md"
    "положение.md" = "docs\положение.md"
}

foreach ($file in $docsFiles.GetEnumerator()) {
    Move-FileSafe $file.Key $file.Value
}

# Перемещение LaTeX файлов
$latexFiles = @{
    "UI\application\latex\result_5pages.tex" = "applications\central-uni\main.tex"
    "UI\application\latex\result.tex" = "applications\central-uni\result_full.tex"
}

foreach ($file in $latexFiles.GetEnumerator()) {
    Move-FileSafe $file.Key $file.Value
}

# Перемещение исследовательских материалов
$researchFiles = @{
    "Osinenko_list_of_papers_no_preprints.bbl" = "research\publications\bibliography.bbl"
    "articles_list.zip" = "research\publications\articles_list.zip"
    "Moduslam_A_Modular_Framework_for_Factor_Graph-Based_Localization_and_Mapping.pdf" = "research\publications\papers\Moduslam_Framework.pdf"
}

foreach ($file in $researchFiles.GetEnumerator()) {
    Move-FileSafe $file.Key $file.Value
}

# Перемещение юридических документов
$legalFiles = @{
    "Сомов пример BioMedTech Lab proposal_20250819_draft.docx" = "legal\other\BioMedTech_Lab_proposal_draft.docx"
    "Положение о конкурсе НС_signed.pdf" = "legal\other\Положение_о_конкурсе_НС_signed.pdf"
}

foreach ($file in $legalFiles.GetEnumerator()) {
    Move-FileSafe $file.Key $file.Value
}

# Перемещение результатов компиляции
$outputFiles = @{
    "result_5pages.pdf" = "output\pdf\result_5pages.pdf"
    "UI\result_5pages.pdf" = "output\pdf\result_5pages_ui.pdf"
}

foreach ($file in $outputFiles.GetEnumerator()) {
    Move-FileSafe $file.Key $file.Value
}

Write-Host "🔧 Создание конфигурационных файлов..." -ForegroundColor Blue

# Создание .gitignore
$gitignore = @"
# LaTeX временные файлы
*.aux
*.log
*.out
*.toc
*.bbl
*.blg
*.synctex.gz
*.fdb_latexmk
*.fls
*.nav
*.snm
*.vrb

# PDF файлы (кроме финальных)
output/pdf/*.pdf
!output/pdf/main.pdf

# Временные файлы
output/temp/
*.tmp

# Системные файлы
.DS_Store
Thumbs.db
~$*

# IDE файлы
.vscode/
.idea/
*.swp
*.swo

# Архивы
*.zip
*.rar
*.7z

# Документы Word
*.docx
*.doc
"@

Set-Content -Path "config\.gitignore" -Value $gitignore -Encoding UTF8
Write-Host "✅ Создан .gitignore" -ForegroundColor Green

# Создание Makefile для Windows
$makefile = @"
# Makefile для Windows (используйте nmake или установите Make для Windows)

# Основные цели
all: clean compile view
compile: output\pdf\main.pdf
clean: clean-temp clean-pdf

# Компиляция
output\pdf\main.pdf: applications\central-uni\main.tex
	@echo Компиляция LaTeX документа...
	pdflatex -output-directory=output\pdf applications\central-uni\main.tex
	bibtex output\pdf\main
	pdflatex -output-directory=output\pdf applications\central-uni\main.tex
	pdflatex -output-directory=output\pdf applications\central-uni\main.tex

# Очистка
clean-temp:
	@if exist output\temp\* del /Q output\temp\*

clean-pdf:
	@if exist output\pdf\*.pdf del /Q output\pdf\*.pdf

# Просмотр
view: output\pdf\main.pdf
	start output\pdf\main.pdf
"@

Set-Content -Path "applications\central-uni\Makefile" -Value $makefile -Encoding UTF8
Write-Host "✅ Создан Makefile для Windows" -ForegroundColor Green

# Создание batch файла для компиляции
$batchFile = @"
@echo off
echo Компиляция LaTeX документа...

REM Проверка наличия pdflatex
where pdflatex >nul 2>nul
if %errorlevel% neq 0 (
    echo ОШИБКА: pdflatex не найден в PATH
    echo Установите MiKTeX или TeX Live
    pause
    exit /b 1
)

REM Создание папки output если её нет
if not exist output\pdf mkdir output\pdf

REM Компиляция
pdflatex -output-directory=output\pdf applications\central-uni\main.tex
if exist output\pdf\main.bib (
    bibtex output\pdf\main
    pdflatex -output-directory=output\pdf applications\central-uni\main.tex
    pdflatex -output-directory=output\pdf applications\central-uni\main.tex
)

echo Компиляция завершена!
if exist output\pdf\main.pdf (
    echo PDF создан: output\pdf\main.pdf
    start output\pdf\main.pdf
) else (
    echo ОШИБКА: PDF не создан
)

pause
"@

Set-Content -Path "applications\central-uni\compile.bat" -Value $batchFile -Encoding UTF8
Write-Host "✅ Создан compile.bat" -ForegroundColor Green

# Создание README для новой структуры
$newReadme = @"
# AIDA-T: Центральный университет - Заявка

## 📁 Новая структура проекта

Проект реорганизован для лучшей навигации и масштабируемости.

### Основные папки:
- `docs/` - Документация проекта
- `applications/` - Заявки и документы
- `research/` - Исследовательские материалы  
- `scripts/` - Скрипты и утилиты
- `presentations/` - Презентации
- `legal/` - Юридические документы
- `output/` - Результаты компиляции

### Компиляция LaTeX документа:

#### Windows (PowerShell):
```powershell
cd applications\central-uni
.\compile.bat
```

#### Windows (Make):
```cmd
cd applications\central-uni
make compile
```

#### Ручная компиляция:
```cmd
pdflatex -output-directory=output\pdf applications\central-uni\main.tex
bibtex output\pdf\main
pdflatex -output-directory=output\pdf applications\central-uni\main.tex
pdflatex -output-directory=output\pdf applications\central-uni\main.tex
```

## 📋 Статус миграции

✅ Структура создана
✅ Файлы перемещены
✅ Конфигурационные файлы созданы
✅ Скрипты компиляции обновлены

## 🔄 Следующие шаги

1. Проверить компиляцию LaTeX документа
2. Обновить ссылки в документах
3. Протестировать все скрипты
4. Обновить документацию
"@

Set-Content -Path "docs\STRUCTURE_MIGRATION.md" -Value $newReadme -Encoding UTF8
Write-Host "✅ Создан STRUCTURE_MIGRATION.md" -ForegroundColor Green

Write-Host "`n🎉 Миграция структуры завершена!" -ForegroundColor Green
Write-Host "📋 Проверьте новую структуру в папке docs\STRUCTURE_MIGRATION.md" -ForegroundColor Cyan
Write-Host "🔧 Для компиляции перейдите в applications\central-uni и запустите compile.bat" -ForegroundColor Cyan

Write-Host "`n📊 Статистика миграции:" -ForegroundColor Blue
Write-Host "- Создано папок: $($folders.Count)" -ForegroundColor White
Write-Host "- Перемещено файлов документации: $($docsFiles.Count)" -ForegroundColor White  
Write-Host "- Перемещено LaTeX файлов: $($latexFiles.Count)" -ForegroundColor White
Write-Host "- Перемещено исследовательских файлов: $($researchFiles.Count)" -ForegroundColor White

Write-Host "`n⚠️  Внимание: Проверьте все перемещенные файлы и обновите ссылки в документах!" -ForegroundColor Yellow
