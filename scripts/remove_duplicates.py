#!/usr/bin/env python3
"""
Скрипт для удаления дублирующихся записей из bib файла.
"""

import re
import sys
from pathlib import Path


def remove_duplicates(input_file, output_file):
    """Удаляет дублирующиеся записи из bib файла."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все записи
    pattern = r'@\w+\{[^}]+\}.*?(?=@\w+\{|$)'
    entries = re.findall(pattern, content, re.DOTALL)
    
    # Создаем словарь для отслеживания уникальных ключей
    unique_entries = {}
    duplicates_found = []
    
    for entry in entries:
        # Извлекаем ключ записи
        key_match = re.search(r'@\w+\{([^,]+)', entry)
        if key_match:
            key = key_match.group(1)
            if key in unique_entries:
                duplicates_found.append(key)
                print(f"Найден дубликат: {key}")
            else:
                unique_entries[key] = entry
    
    # Создаем новый контент без дубликатов
    new_content = '\n\n'.join(unique_entries.values())
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Файл исправлен: {output_file}")
    print(f"Удалено дубликатов: {len(duplicates_found)}")
    print(f"Осталось уникальных записей: {len(unique_entries)}")


def main():
    """Основная функция для запуска скрипта."""
    if len(sys.argv) != 3:
        print("Использование: python remove_duplicates.py input.bib output.bib")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    
    remove_duplicates(input_file, output_file)


if __name__ == "__main__":
    main()
