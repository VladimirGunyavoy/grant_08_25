@echo off
echo 🚀 Начинаем миграцию структуры проекта AIDA-T...
echo.

REM Создание основной структуры папок
echo 📁 Создание новой структуры папок...

mkdir docs 2>nul
mkdir applications\central-uni\assets 2>nul
mkdir applications\central-uni\sections 2>nul
mkdir applications\start-ii 2>nul
mkdir applications\other 2>nul
mkdir research\publications\papers 2>nul
mkdir research\technical\diagrams 2>nul
mkdir research\data\datasets 2>nul
mkdir scripts 2>nul
mkdir presentations\aida-t 2>nul
mkdir presentations\general 2>nul
mkdir legal\ooo 2>nul
mkdir legal\residency 2>nul
mkdir config 2>nul
mkdir output\pdf 2>nul
mkdir output\temp 2>nul

echo ✅ Папки созданы
echo.

echo 📄 Перемещение файлов...

REM Перемещение документации
if exist README.md (
    move README.md docs\ >nul
    echo ✅ Перемещен README.md
)
if exist STATUS.md (
    move STATUS.md docs\ >nul
    echo ✅ Перемещен STATUS.md
)
if exist SUMMARY.md (
    move SUMMARY.md docs\ >nul
    echo ✅ Перемещен SUMMARY.md
)
if exist INSTALL.md (
    move INSTALL.md docs\ >nul
    echo ✅ Перемещен INSTALL.md
)
if exist PERL_FIX.md (
    move PERL_FIX.md docs\ >nul
    echo ✅ Перемещен PERL_FIX.md
)
if exist "Описание_результатов_исследований.md" (
    move "Описание_результатов_исследований.md" docs\ >nul
    echo ✅ Перемещен Описание_результатов_исследований.md
)
if exist "положение.md" (
    move "положение.md" docs\ >nul
    echo ✅ Перемещен положение.md
)

REM Перемещение LaTeX файлов
if exist "UI\application\latex\result_5pages.tex" (
    move "UI\application\latex\result_5pages.tex" "applications\central-uni\main.tex" >nul
    echo ✅ Перемещен result_5pages.tex -> main.tex
)
if exist "UI\application\latex\result.tex" (
    move "UI\application\latex\result.tex" "applications\central-uni\result_full.tex" >nul
    echo ✅ Перемещен result.tex -> result_full.tex
)

REM Перемещение исследовательских материалов
if exist "Osinenko_list_of_papers_no_preprints.bbl" (
    move "Osinenko_list_of_papers_no_preprints.bbl" "research\publications\bibliography.bbl" >nul
    echo ✅ Перемещен bibliography.bbl
)
if exist "articles_list.zip" (
    move "articles_list.zip" "research\publications\" >nul
    echo ✅ Перемещен articles_list.zip
)
if exist "Moduslam_A_Modular_Framework_for_Factor_Graph-Based_Localization_and_Mapping.pdf" (
    move "Moduslam_A_Modular_Framework_for_Factor_Graph-Based_Localization_and_Mapping.pdf" "research\publications\papers\Moduslam_Framework.pdf" >nul
    echo ✅ Перемещен Moduslam Framework
)

REM Перемещение юридических документов
if exist "Сомов пример BioMedTech Lab proposal_20250819_draft.docx" (
    move "Сомов пример BioMedTech Lab proposal_20250819_draft.docx" "legal\other\BioMedTech_Lab_proposal_draft.docx" >nul
    echo ✅ Перемещен BioMedTech proposal
)
if exist "Положение о конкурсе НС_signed.pdf" (
    move "Положение о конкурсе НС_signed.pdf" "legal\other\" >nul
    echo ✅ Перемещен Положение о конкурсе
)

REM Перемещение результатов компиляции
if exist "result_5pages.pdf" (
    move "result_5pages.pdf" "output\pdf\" >nul
    echo ✅ Перемещен result_5pages.pdf
)
if exist "UI\result_5pages.pdf" (
    move "UI\result_5pages.pdf" "output\pdf\result_5pages_ui.pdf" >nul
    echo ✅ Перемещен result_5pages_ui.pdf
)

echo.
echo 🔧 Создание конфигурационных файлов...

REM Создание .gitignore
echo # LaTeX временные файлы > config\.gitignore
echo *.aux >> config\.gitignore
echo *.log >> config\.gitignore
echo *.out >> config\.gitignore
echo *.toc >> config\.gitignore
echo *.bbl >> config\.gitignore
echo *.blg >> config\.gitignore
echo *.synctex.gz >> config\.gitignore
echo *.fdb_latexmk >> config\.gitignore
echo *.fls >> config\.gitignore
echo *.nav >> config\.gitignore
echo *.snm >> config\.gitignore
echo *.vrb >> config\.gitignore
echo. >> config\.gitignore
echo # PDF файлы >> config\.gitignore
echo output/pdf/*.pdf >> config\.gitignore
echo !output/pdf/main.pdf >> config\.gitignore
echo. >> config\.gitignore
echo # Временные файлы >> config\.gitignore
echo output/temp/ >> config\.gitignore
echo *.tmp >> config\.gitignore
echo. >> config\.gitignore
echo # Системные файлы >> config\.gitignore
echo .DS_Store >> config\.gitignore
echo Thumbs.db >> config\.gitignore
echo ~$* >> config\.gitignore
echo. >> config\.gitignore
echo # IDE файлы >> config\.gitignore
echo .vscode/ >> config\.gitignore
echo .idea/ >> config\.gitignore
echo *.swp >> config\.gitignore
echo *.swo >> config\.gitignore
echo. >> config\.gitignore
echo # Архивы >> config\.gitignore
echo *.zip >> config\.gitignore
echo *.rar >> config\.gitignore
echo *.7z >> config\.gitignore
echo. >> config\.gitignore
echo # Документы Word >> config\.gitignore
echo *.docx >> config\.gitignore
echo *.doc >> config\.gitignore

echo ✅ Создан .gitignore

REM Создание batch файла для компиляции
echo @echo off > "applications\central-uni\compile.bat"
echo echo Компиляция LaTeX документа... >> "applications\central-uni\compile.bat"
echo. >> "applications\central-uni\compile.bat"
echo REM Проверка наличия pdflatex >> "applications\central-uni\compile.bat"
echo where pdflatex ^>nul 2^>nul >> "applications\central-uni\compile.bat"
echo if %%errorlevel%% neq 0 ^( >> "applications\central-uni\compile.bat"
echo     echo ОШИБКА: pdflatex не найден в PATH >> "applications\central-uni\compile.bat"
echo     echo Установите MiKTeX или TeX Live >> "applications\central-uni\compile.bat"
echo     pause >> "applications\central-uni\compile.bat"
echo     exit /b 1 >> "applications\central-uni\compile.bat"
echo ^) >> "applications\central-uni\compile.bat"
echo. >> "applications\central-uni\compile.bat"
echo REM Создание папки output если её нет >> "applications\central-uni\compile.bat"
echo if not exist output\pdf mkdir output\pdf >> "applications\central-uni\compile.bat"
echo. >> "applications\central-uni\compile.bat"
echo REM Компиляция >> "applications\central-uni\compile.bat"
echo pdflatex -output-directory=output\pdf applications\central-uni\main.tex >> "applications\central-uni\compile.bat"
echo if exist output\pdf\main.bib ^( >> "applications\central-uni\compile.bat"
echo     bibtex output\pdf\main >> "applications\central-uni\compile.bat"
echo     pdflatex -output-directory=output\pdf applications\central-uni\main.tex >> "applications\central-uni\compile.bat"
echo     pdflatex -output-directory=output\pdf applications\central-uni\main.tex >> "applications\central-uni\compile.bat"
echo ^) >> "applications\central-uni\compile.bat"
echo. >> "applications\central-uni\compile.bat"
echo echo Компиляция завершена! >> "applications\central-uni\compile.bat"
echo if exist output\pdf\main.pdf ^( >> "applications\central-uni\compile.bat"
echo     echo PDF создан: output\pdf\main.pdf >> "applications\central-uni\compile.bat"
echo     start output\pdf\main.pdf >> "applications\central-uni\compile.bat"
echo ^) else ^( >> "applications\central-uni\compile.bat"
echo     echo ОШИБКА: PDF не создан >> "applications\central-uni\compile.bat"
echo ^) >> "applications\central-uni\compile.bat"
echo. >> "applications\central-uni\compile.bat"
echo pause >> "applications\central-uni\compile.bat"

echo ✅ Создан compile.bat

echo.
echo 🎉 Миграция структуры завершена!
echo.
echo 📋 Следующие шаги:
echo 1. Перейдите в папку applications\central-uni
echo 2. Запустите compile.bat для проверки компиляции
echo 3. Проверьте все перемещенные файлы
echo 4. Обновите ссылки в документах
echo.
echo ⚠️  Внимание: Проверьте все перемещенные файлы и обновите ссылки в документах!
echo.
pause
