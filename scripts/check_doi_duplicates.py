#!/usr/bin/env python3
import re
import json
from collections import defaultdict

def parse_bibtex_dois(bibtex_file):
    """Парсит BibTeX файл и извлекает DOI статей"""
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
                
                # Извлекаем DOI
                doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry)
                if doi_match:
                    doi = doi_match.group(1).strip()
                    articles.append({
                        'key': key,
                        'doi': doi,
                        'entry': entry.strip()
                    })
    
    return articles

def find_doi_duplicates(articles):
    """Находит статьи с одинаковыми DOI"""
    doi_groups = defaultdict(list)
    
    for article in articles:
        doi_groups[article['doi']].append(article)
    
    # Возвращаем только группы с более чем одной статьей
    duplicates = {doi: articles for doi, articles in doi_groups.items() if len(articles) > 1}
    return duplicates

def main():
    bibtex_file = 'central uni grant/my_bib.bib'
    
    print("🔍 Анализ дублирующихся DOI в BibTeX файле...")
    print("=" * 80)
    
    articles = parse_bibtex_dois(bibtex_file)
    print(f"📊 Всего статей с DOI в файле: {len(articles)}")
    
    duplicates = find_doi_duplicates(articles)
    
    if not duplicates:
        print("✅ Дублирующихся DOI не найдено!")
        return
    
    print(f"\n⚠️  Найдено {len(duplicates)} групп статей с одинаковыми DOI:")
    print("=" * 80)
    
    for i, (doi, articles) in enumerate(duplicates.items(), 1):
        print(f"\n{i}. DOI: {doi}")
        print("-" * 60)
        
        for j, article in enumerate(articles, 1):
            print(f"   {j}. Ключ: {article['key']}")
            print()
    
    # Сохраняем результаты в JSON для дальнейшего анализа
    results = {
        'total_articles_with_doi': len(articles),
        'duplicate_doi_groups': len(duplicates),
        'duplicates': {
            doi: [{'key': a['key']} for a in articles]
            for doi, articles in duplicates.items()
        }
    }
    
    with open('doi_duplicate_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Результаты сохранены в файл: doi_duplicate_analysis.json")

if __name__ == "__main__":
    main()
