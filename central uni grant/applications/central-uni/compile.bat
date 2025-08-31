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
if not exist ..\..\output\pdf mkdir ..\..\output\pdf

REM Компиляция
pdflatex -output-directory=..\..\output\pdf main.tex
if exist ..\..\output\pdf\main.bib (
    bibtex ..\..\output\pdf\main
    pdflatex -output-directory=..\..\output\pdf main.tex
    pdflatex -output-directory=..\..\output\pdf main.tex
)

echo Компиляция завершена!
if exist ..\..\output\pdf\main.pdf (
    echo PDF создан: ..\..\output\pdf\main.pdf
    start ..\..\output\pdf\main.pdf
) else (
    echo ОШИБКА: PDF не создан
)

pause
