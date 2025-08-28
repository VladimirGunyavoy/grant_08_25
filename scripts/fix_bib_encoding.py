#!/usr/bin/env python3
"""
Скрипт для исправления проблем с кодировкой в bib файле.

Исправляет записи с русским текстом для совместимости с LaTeX.
"""

import re
import sys
from pathlib import Path


def fix_bib_encoding(input_file, output_file):
    """Исправляет проблемы с кодировкой в bib файле."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем записи с русским текстом
    replacements = [
        # Первая запись
        (
            r'@article\{совершенствование_методики_обработки_данных_2011,',
            r'@article{improving_data_processing_methods_2011,'
        ),
        (
            r'title = \{Совершенствование методики обработки данных испытаний наземных транспортных средств\},',
            r'title = {Improving data processing methods for ground vehicle testing},'
        ),
        (
            r'author = \{Осиненко П\.В\.\},',
            r'author = {Osinenko P.V.},'
        ),
        (
            r'journal = \{Тракторы и сельхозмашины\},',
            r'journal = {Tractors and Agricultural Machines},'
        ),
        (
            r'address = \{Калужский ф-л МГТУ им\. Н\.Э\. Баумана\},',
            r'address = {Kaluga Branch of Bauman Moscow State Technical University},'
        ),
        (
            r'publisher = \{Московский политехнический университет, ООО "Эко-Вектор"\},',
            r'publisher = {Moscow Polytechnic University, Eco-Vector LLC},'
        ),
        (
            r'note = \{УДК: 629\.114\.2\}',
            r'note = {UDC: 629.114.2}'
        ),
        
        # Вторая запись
        (
            r'@article\{усовершенствованная_измерительная_система_для_2012,',
            r'@article{improved_measurement_system_for_2012,'
        ),
        (
            r'title = \{Усовершенствованная измерительная система для наземно-транспортных средств\},',
            r'title = {Improved measurement system for ground vehicles},'
        ),
        (
            r'author = \{П\.В\. Осиненко and В\.А\. Воронин and М\.В\. Сидоров\},',
            r'author = {P.V. Osinenko and V.A. Voronin and M.V. Sidorov},'
        ),
        (
            r'journal = \{Сельскохозяйственные машины и технологии\},',
            r'journal = {Agricultural Machines and Technologies},'
        ),
        (
            r'publisher = \{Федеральный научный агроинженерный центр ВИМ\},',
            r'publisher = {Federal Scientific Agroengineering Center VIM},'
        ),
        (
            r'note = \{КФ МГТУ им\. Н\.Э\. Баумана\}',
            r'note = {KF Bauman Moscow State Technical University}'
        )
    ]
    
    # Применяем замены
    for old_pattern, new_pattern in replacements:
        content = re.sub(old_pattern, new_pattern, content)
    
    # Удаляем строки с language = {russian}
    content = re.sub(r'language = \{russian\},?\n?', '', content)
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Файл исправлен: {output_file}")
    print("Русский текст заменен на английский для совместимости с LaTeX")


def main():
    """Основная функция для запуска скрипта."""
    if len(sys.argv) != 3:
        print("Использование: python fix_bib_encoding.py input.bib output.bib")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    
    fix_bib_encoding(input_file, output_file)


if __name__ == "__main__":
    main()
