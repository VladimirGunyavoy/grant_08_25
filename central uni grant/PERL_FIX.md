# 🔧 Решение проблемы с Perl для LaTeX

## Проблема
```
MiKTeX could not find the script engine 'perl' which is required to execute 'latexmk'.
```

## Решения

### 1. Установить Perl (рекомендуется)

#### Windows
1. **Скачайте Strawberry Perl**: https://strawberryperl.com/
2. **Выберите версию**: 64-bit для Windows 10/11
3. **Установите** с настройками по умолчанию
4. **Перезапустите** PowerShell/командную строку

#### Альтернативно - через Chocolatey:
```powershell
choco install strawberryperl
```

### 2. Использовать pdflatex напрямую (обходное решение)

Вместо `latexmk` используйте `pdflatex` напрямую:

#### PowerShell:
```powershell
# Компиляция в 2 прохода
pdflatex -interaction=nonstopmode Описание_результатов_исследований.tex
pdflatex -interaction=nonstopmode Описание_результатов_исследований.tex
```

#### Или используйте наши скрипты:
```powershell
.\compile.ps1 all
```

### 3. Настройка VS Code/Cursor

#### Отключить latexmk в LaTeX Workshop:
1. Откройте настройки VS Code/Cursor
2. Найдите `latex-workshop.latex.tools`
3. Измените настройки:

```json
{
    "latex-workshop.latex.tools": [
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "latex-workshop.latex.recipes": [
        {
            "name": "pdflatex",
            "tools": [
                "pdflatex",
                "pdflatex"
            ]
        }
    ]
}
```

### 4. Проверка установки

После установки Perl проверьте:

```powershell
# Проверка Perl
perl --version

# Проверка latexmk
latexmk --version

# Проверка pdflatex
pdflatex --version
```

### 5. Альтернативные компиляторы

Если проблемы продолжаются, используйте:

#### XeLaTeX (лучшая поддержка Unicode):
```powershell
xelatex -interaction=nonstopmode Описание_результатов_исследований.tex
```

#### LuaLaTeX:
```powershell
lualatex -interaction=nonstopmode Описание_результатов_исследований.tex
```

## Рекомендации

1. **Установите Strawberry Perl** - это самое надежное решение
2. **Используйте наши скрипты** - они работают без latexmk
3. **Настройте VS Code** для использования pdflatex напрямую
4. **Перезапустите терминал** после установки Perl

## Проверка решения

После установки Perl попробуйте:

```powershell
# Проверка зависимостей
.\compile.ps1 check

# Компиляция
.\compile.ps1 all
```

Если все работает, вы увидите:
```
LaTeX found: C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe
Compiling LaTeX document...
Pass 1 of 2...
Pass 2 of 2...
Document compiled successfully!
```
