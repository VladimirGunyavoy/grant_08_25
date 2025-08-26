#!/usr/bin/env python3
import re
import json
from collections import defaultdict

def parse_bibtex(bibtex_file):
    """Парсит BibTeX файл и извлекает названия статей"""
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Разбиваем на отдельные записи
    entries = re.split(r'\n(?=@)', content)
    
    articles = []
    for entry in entries:
        if entry.strip() and entry.startswith('@'):
            # Извлекаем ключ записи
            key_match = re.search(r'@\w+\{([^,]+),', entry)
            if key_match:
                key = key_match.group(1)
                
                # Извлекаем название
                title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry)
                if title_match:
                    title = title_match.group(1).strip()
                    articles.append({
                        'key': key,
                        'title': title,
                        'entry': entry.strip()
                    })
    
    return articles

def find_duplicates(articles):
    """Находит статьи с одинаковыми названиями"""
    title_groups = defaultdict(list)
    
    for article in articles:
        # Нормализуем название (убираем лишние пробелы, приводим к нижнему регистру)
        normalized_title = re.sub(r'\s+', ' ', article['title'].lower().strip())
        title_groups[normalized_title].append(article)
    
    # Возвращаем только группы с более чем одной статьей
    duplicates = {title: articles for title, articles in title_groups.items() if len(articles) > 1}
    return duplicates

def main():
    bibtex_file = 'central uni grant/my_bib.bib'
    
    print("🔍 Анализ дублирующихся названий статей в BibTeX файле...")
    print("=" * 80)
    
    articles = parse_bibtex(bibtex_file)
    print(f"📊 Всего статей в файле: {len(articles)}")
    
    duplicates = find_duplicates(articles)
    
    if not duplicates:
        print("✅ Дублирующихся названий не найдено!")
        return
    
    print(f"\n⚠️  Найдено {len(duplicates)} групп статей с одинаковыми названиями:")
    print("=" * 80)
    
    for i, (title, articles) in enumerate(duplicates.items(), 1):
        print(f"\n{i}. Название: {title}")
        print("-" * 60)
        
        for j, article in enumerate(articles, 1):
            print(f"   {j}. Ключ: {article['key']}")
            print(f"      Оригинальное название: {article['title']}")
            print()
    
    # Сохраняем результаты в JSON для дальнейшего анализа
    results = {
        'total_articles': len(articles),
        'duplicate_groups': len(duplicates),
        'duplicates': {
            title: [{'key': a['key'], 'title': a['title']} for a in articles]
            for title, articles in duplicates.items()
        }
    }
    
    with open('duplicate_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Результаты сохранены в файл: duplicate_analysis.json")

if __name__ == "__main__":
    main()
