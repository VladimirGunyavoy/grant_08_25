#!/usr/bin/env python3
"""
Скрипт для обновления ключей цитирования в LaTeX файле.

Обновляет старые ключи (фамилия+год) на новые семантические ключи
после преобразования bib файла.
"""

import re
import sys
from pathlib import Path


def create_key_mapping(bib_file):
    """Создает отображение старых ключей на новые из bib файла."""
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Паттерн для поиска старых ключей (фамилия+год)
    old_pattern = r'@\w+\{([A-Z][a-z]+[0-9]+)'
    old_keys = set(re.findall(old_pattern, content))
    
    # Паттерн для поиска новых ключей (семантические)
    new_pattern = r'@\w+\{([a-z_]+_[0-9]+)'
    new_keys = set(re.findall(new_pattern, content))
    
    # Создаем отображение (это упрощенная версия, в реальности нужно
    # сопоставлять по заголовкам)
    mapping = {}
    
    # Для демонстрации создадим базовое отображение
    # В реальности нужно анализировать заголовки статей
    print("Найдены старые ключи:", sorted(old_keys))
    print("Найдены новые ключи:", sorted(new_keys))
    
    return mapping


def update_latex_citations(latex_file, bib_file, output_file):
    """Обновляет ключи цитирования в LaTeX файле."""
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Создаем отображение ключей
    mapping = create_key_mapping(bib_file)
    
    # Заменяем старые ключи на новые
    for old_key, new_key in mapping.items():
        content = content.replace(f'\\nocite{{{old_key}}}', f'\\nocite{{{new_key}}}')
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Файл обновлен: {output_file}")


def main():
    """Основная функция для запуска скрипта."""
    if len(sys.argv) != 4:
        print("Использование: python update_latex_citations.py latex_file.tex bib_file.bib output_file.tex")
        sys.exit(1)
    
    latex_file = sys.argv[1]
    bib_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if not Path(latex_file).exists():
        print(f"Ошибка: файл {latex_file} не найден")
        sys.exit(1)
    
    if not Path(bib_file).exists():
        print(f"Ошибка: файл {bib_file} не найден")
        sys.exit(1)
    
    update_latex_citations(latex_file, bib_file, output_file)


if __name__ == "__main__":
    main()
