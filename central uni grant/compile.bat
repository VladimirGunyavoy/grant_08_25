@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set TARGET=Описание_результатов_исследований
set LATEX=pdflatex

echo.
echo ========================================
echo    Компиляция LaTeX документа AIDA-T
echo ========================================
echo.

if "%1"=="" (
    echo Использование: compile.bat [команда]
    echo.
    echo Доступные команды:
    echo   all    - Полная компиляция (2 прохода)
    echo   quick  - Быстрая компиляция (1 проход)
    echo   clean  - Очистка временных файлов
    echo   check  - Проверка LaTeX
    echo.
    goto :eof
)

if "%1"=="check" (
    echo Проверка наличия LaTeX...
    where %LATEX% >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✓ LaTeX найден
        for /f "tokens=*" %%i in ('where %LATEX%') do echo   %%i
    ) else (
        echo ✗ LaTeX не найден
        echo.
        echo Установите MiKTeX или TeX Live:
        echo   MiKTeX: https://miktex.org/download
        echo   TeX Live: https://www.tug.org/texlive/
        echo.
        echo После установки перезапустите командную строку
    )
    goto :eof
)

if "%1"=="clean" (
    echo Очистка временных файлов...
    del /q "%TARGET%.aux" "%TARGET%.log" "%TARGET%.out" "%TARGET%.toc" 2>nul
    del /q "%TARGET%.lot" "%TARGET%.lof" "%TARGET%.blg" "%TARGET%.bbl" 2>nul
    del /q "%TARGET%.bcf" "%TARGET%.run.xml" "%TARGET%.fdb_latexmk" 2>nul
    del /q "%TARGET%.fls" "%TARGET%.synctex.gz" 2>nul
    echo ✓ Временные файлы удалены
    goto :eof
)

if "%1"=="quick" (
    echo Быстрая компиляция (1 проход)...
    %LATEX% -interaction=nonstopmode "%TARGET%.tex"
    if !errorlevel! equ 0 (
        echo ✓ Документ скомпилирован
    ) else (
        echo ✗ Ошибка компиляции
    )
    goto :eof
)

if "%1"=="all" (
    echo Полная компиляция (2 прохода)...
    echo Проход 1 из 2...
    %LATEX% -interaction=nonstopmode "%TARGET%.tex"
    if !errorlevel! neq 0 (
        echo ✗ Ошибка на первом проходе
        goto :eof
    )
    echo Проход 2 из 2...
    %LATEX% -interaction=nonstopmode "%TARGET%.tex"
    if !errorlevel! equ 0 (
        echo ✓ Документ успешно скомпилирован
        if exist "%TARGET%.pdf" (
            echo ✓ PDF файл создан: %TARGET%.pdf
        )
    ) else (
        echo ✗ Ошибка на втором проходе
    )
    goto :eof
)

echo Неизвестная команда: %1
echo Используйте: compile.bat help
