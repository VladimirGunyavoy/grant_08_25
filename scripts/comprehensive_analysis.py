#!/usr/bin/env python3
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

def parse_bibtex_comprehensive(bibtex_file):
    """Парсит BibTeX файл и извлекает полную информацию о статьях"""
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
                
                # Извлекаем различные поля
                title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry)
                author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry)
                journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', entry)
                year_match = re.search(r'year\s*=\s*\{([^}]+)\}', entry)
                doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry)
                volume_match = re.search(r'volume\s*=\s*\{([^}]+)\}', entry)
                pages_match = re.search(r'pages\s*=\s*\{([^}]+)\}', entry)
                publisher_match = re.search(r'publisher\s*=\s*\{([^}]+)\}', entry)
                
                article_data = {
                    'key': key,
                    'title': title_match.group(1).strip() if title_match else None,
                    'author': author_match.group(1).strip() if author_match else None,
                    'journal': journal_match.group(1).strip() if journal_match else None,
                    'year': year_match.group(1).strip() if year_match else None,
                    'doi': doi_match.group(1).strip() if doi_match else None,
                    'volume': volume_match.group(1).strip() if volume_match else None,
                    'pages': pages_match.group(1).strip() if pages_match else None,
                    'publisher': publisher_match.group(1).strip() if publisher_match else None,
                }
                
                articles.append(article_data)
    
    return articles

def analyze_articles(articles):
    """Анализирует статьи и создает статистику"""
    
    # Статистика по годам
    years = [int(article['year']) for article in articles if article['year'] and article['year'].isdigit()]
    year_stats = Counter(years)
    
    # Статистика по журналам
    journals = [article['journal'] for article in articles if article['journal']]
    journal_stats = Counter(journals)
    
    # Статистика по издателям
    publishers = [article['publisher'] for article in articles if article['publisher']]
    publisher_stats = Counter(publishers)
    
    # Анализ авторов (первый автор)
    first_authors = []
    for article in articles:
        if article['author']:
            # Извлекаем первого автора
            authors = article['author'].split(' and ')
            if authors:
                first_author = authors[0].strip()
                if 'Osinenko' in first_author:
                    first_authors.append(article['year'])
    
    first_author_stats = Counter(first_authors)
    
    # Проверка на дубликаты
    titles = [article['title'].lower().strip() if article['title'] else '' for article in articles]
    title_duplicates = [title for title, count in Counter(titles).items() if count > 1]
    
    dois = [article['doi'] for article in articles if article['doi']]
    doi_duplicates = [doi for doi, count in Counter(dois).items() if count > 1]
    
    keys = [article['key'] for article in articles]
    key_duplicates = [key for key, count in Counter(keys).items() if count > 1]
    
    return {
        'total_articles': len(articles),
        'years': year_stats,
        'journals': journal_stats,
        'publishers': publisher_stats,
        'first_authors': first_author_stats,
        'title_duplicates': title_duplicates,
        'doi_duplicates': doi_duplicates,
        'key_duplicates': key_duplicates,
        'articles': articles
    }

def main():
    bibtex_file = 'central uni grant/my_bib.bib'
    
    print("🔍 Комплексный анализ BibTeX файла...")
    print("=" * 80)
    
    articles = parse_bibtex_comprehensive(bibtex_file)
    analysis = analyze_articles(articles)
    
    print(f"📊 Общая статистика:")
    print(f"   Всего статей: {analysis['total_articles']}")
    print(f"   Период: {min(analysis['years'].keys())} - {max(analysis['years'].keys())}")
    
    print(f"\n📅 Публикации по годам:")
    for year in sorted(analysis['years'].keys()):
        count = analysis['years'][year]
        first_author_count = analysis['first_authors'].get(str(year), 0)
        print(f"   {year}: {count} статей ({first_author_count} первым автором)")
    
    print(f"\n📚 Топ-10 журналов:")
    for journal, count in analysis['journals'].most_common(10):
        print(f"   {journal}: {count} статей")
    
    print(f"\n🏢 Топ-5 издателей:")
    for publisher, count in analysis['publishers'].most_common(5):
        print(f"   {publisher}: {count} статей")
    
    print(f"\n🔍 Проверка дубликатов:")
    print(f"   Дублирующихся названий: {len(analysis['title_duplicates'])}")
    print(f"   Дублирующихся DOI: {len(analysis['doi_duplicates'])}")
    print(f"   Дублирующихся ключей: {len(analysis['key_duplicates'])}")
    
    if analysis['title_duplicates']:
        print(f"\n⚠️  Дублирующиеся названия:")
        for title in analysis['title_duplicates']:
            print(f"   - {title}")
    
    if analysis['doi_duplicates']:
        print(f"\n⚠️  Дублирующиеся DOI:")
        for doi in analysis['doi_duplicates']:
            print(f"   - {doi}")
    
    if analysis['key_duplicates']:
        print(f"\n⚠️  Дублирующиеся ключи:")
        for key in analysis['key_duplicates']:
            print(f"   - {key}")
    
    # Сохраняем полный анализ
    results = {
        'analysis_date': datetime.now().isoformat(),
        'total_articles': analysis['total_articles'],
        'year_range': f"{min(analysis['years'].keys())} - {max(analysis['years'].keys())}",
        'years': dict(analysis['years']),
        'journals': dict(analysis['journals']),
        'publishers': dict(analysis['publishers']),
        'first_authors': dict(analysis['first_authors']),
        'duplicates': {
            'titles': analysis['title_duplicates'],
            'dois': analysis['doi_duplicates'],
            'keys': analysis['key_duplicates']
        },
        'articles': analysis['articles']
    }
    
    with open('comprehensive_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Полный анализ сохранен в файл: comprehensive_analysis.json")

if __name__ == "__main__":
    main()
