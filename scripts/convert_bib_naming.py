#!/usr/bin/env python3
"""
Скрипт для преобразования именования библиографических записей.

Преобразует формат "фамилия год" на формат, основанный на начале
заголовка статьи.
"""

import re
import sys
from pathlib import Path


def clean_title_for_key(title):
    """Очищает заголовок для использования в качестве ключа."""
    # Убираем специальные символы и приводим к нижнему регистру
    cleaned = re.sub(r'[^\w\s]', '', title.lower())
    # Заменяем пробелы на подчеркивания
    cleaned = re.sub(r'\s+', '_', cleaned)
    # Берем первые 3-4 слова
    words = cleaned.split('_')
    if len(words) >= 4:
        return '_'.join(words[:4])
    else:
        return cleaned


def convert_bib_naming(input_file, output_file):
    """Преобразует именование в bib файле."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Паттерн для поиска bib записей
    pattern = r'@(\w+)\{([^,]+),\s*\n\s*title\s*=\s*\{([^}]+)\}'
    
    def replace_entry(match):
        entry_type = match.group(1)
        old_key = match.group(2)
        title = match.group(3)
        
        # Создаем новый ключ на основе заголовка
        new_key = clean_title_for_key(title)
        
        # Добавляем год к ключу для уникальности
        year_match = re.search(
            r'year\s*=\s*\{(\d{4})\}', 
            content[match.start():match.start()+500]
        )
        if year_match:
            year = year_match.group(1)
            new_key = f"{new_key}_{year}"
        
        print(f"Преобразование: {old_key} -> {new_key}")
        print(f"  Заголовок: {title}")
        
        # Заменяем ключ в записи
        return f"@{entry_type}{{{new_key},"
    
    # Выполняем замену
    new_content = re.sub(
        pattern, replace_entry, content, flags=re.MULTILINE | re.DOTALL
    )
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nФайл сохранен как: {output_file}")


def main():
    """Основная функция для запуска скрипта."""
    if len(sys.argv) != 3:
        print("Использование: python convert_bib_naming.py input.bib output.bib")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    
    convert_bib_naming(input_file, output_file)


if __name__ == "__main__":
    main()
