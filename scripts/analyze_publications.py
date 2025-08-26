#!/usr/bin/env python3
"""
Script to analyze publication statistics from BibTeX file
"""

import re
import json
from collections import defaultdict, Counter

def parse_bibtex_file(filename):
    """Parse BibTeX file and extract publication data"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into individual entries
    entries = re.split(r'\n(?=@)', content)
    
    publications = []
    
    for entry in entries:
        if not entry.strip() or not entry.startswith('@'):
            continue
        
        # Extract basic information
        title_match = re.search(r'title\s*=\s*{([^}]+)}', entry)
        author_match = re.search(r'author\s*=\s*{([^}]+)}', entry)
        year_match = re.search(r'year\s*=\s*{([^}]+)}', entry)
        journal_match = re.search(r'journal\s*=\s*{([^}]+)}', entry)
        doi_match = re.search(r'doi\s*=\s*{([^}]+)}', entry)
        
        if title_match and author_match and year_match:
            title = title_match.group(1).strip()
            authors = [author.strip() for author in author_match.group(1).split(' and ')]
            year = year_match.group(1).strip()
            journal = journal_match.group(1).strip() if journal_match else ""
            doi = doi_match.group(1).strip() if doi_match else ""
            
            # Determine if first author
            is_first_author = False
            if authors:
                first_author = authors[0].lower()
                if 'osinenko' in first_author or 'павел' in first_author or 'pavel' in first_author:
                    is_first_author = True
            
            publications.append({
                'title': title,
                'authors': authors,
                'year': year,
                'journal': journal,
                'doi': doi,
                'is_first_author': is_first_author
            })
    
    return publications

def analyze_publications(publications):
    """Analyze publication statistics"""
    stats = {}
    
    # Basic counts
    stats['total_publications'] = len(publications)
    stats['first_author_publications'] = sum(1 for p in publications if p['is_first_author'])
    
    # Years
    years = [int(p['year']) for p in publications if p['year'].isdigit()]
    stats['year_range'] = f"{min(years)}-{max(years)}" if years else "N/A"
    stats['avg_per_year'] = round(len(publications) / (max(years) - min(years) + 1), 1) if years else 0
    
    # Publications by year
    year_counts = Counter(int(p['year']) for p in publications if p['year'].isdigit())
    stats['by_year'] = dict(sorted(year_counts.items()))
    
    # First author by year
    first_author_by_year = Counter()
    for p in publications:
        if p['is_first_author'] and p['year'].isdigit():
            first_author_by_year[int(p['year'])] += 1
    stats['first_author_by_year'] = dict(sorted(first_author_by_year.items()))
    
    # Journals
    journal_counts = Counter(p['journal'] for p in publications if p['journal'])
    stats['top_journals'] = dict(journal_counts.most_common(10))
    
    # Research areas (based on journal names and titles)
    research_areas = {
        'control_theory': 0,
        'machine_learning': 0,
        'agriculture': 0,
        'optimization': 0,
        'energy': 0
    }
    
    for p in publications:
        title_lower = p['title'].lower()
        journal_lower = p['journal'].lower()
        
        # Control theory and automation
        if any(keyword in title_lower or keyword in journal_lower 
               for keyword in ['control', 'automatic', 'ifac', 'ecc', 'cdc']):
            research_areas['control_theory'] += 1
        
        # Machine learning and AI
        if any(keyword in title_lower or keyword in journal_lower 
               for keyword in ['learning', 'reinforcement', 'neural', 'ai', 'artificial']):
            research_areas['machine_learning'] += 1
        
        # Agriculture
        if any(keyword in title_lower or keyword in journal_lower 
               for keyword in ['biosystem', 'agriculture', 'farm', 'tractor', 'soil']):
            research_areas['agriculture'] += 1
        
        # Optimization
        if any(keyword in title_lower or keyword in journal_lower 
               for keyword in ['optimization', 'optimal', 'dynamic programming']):
            research_areas['optimization'] += 1
        
        # Energy
        if any(keyword in title_lower or keyword in journal_lower 
               for keyword in ['energy', 'battery', 'flow']):
            research_areas['energy'] += 1
    
    stats['research_areas'] = research_areas
    
    return stats

def generate_latex_tables(stats):
    """Generate LaTeX table content"""
    
    # Basic statistics table
    basic_stats = f"""\\begin{{table}}[h]
\\centering
\\begin{{tabular}}{{|l|c|}}
\\hline
\\textbf{{Метрика}} & \\textbf{{Значение}} \\\\
\\hline
Всего публикаций & {stats['total_publications']} \\\\
\\hline
Публикаций первым автором & {stats['first_author_publications']} \\\\
\\hline
Период публикаций & {stats['year_range']} \\\\
\\hline
Среднее количество публикаций в год & {stats['avg_per_year']} \\\\
\\hline
\\end{{tabular}}
\\end{{table}}"""

    # Citation statistics table
    citation_stats = """\\begin{table}[h]
\\centering
\\begin{tabular}{|l|c|c|}
\\hline
\\textbf{Метрика} & \\textbf{Все} & \\textbf{Начиная с 2020 г.} \\\\
\\hline
Процитировано & 512 & 428 \\\\
\\hline
h-индекс & 11 & 11 \\\\
\\hline
i10-индекс & 14 & 12 \\\\
\\hline
\\end{tabular}
\\end{table}"""
    
    # Publications by year table
    year_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|c|c|c|}\n\\hline\n\\textbf{Год} & \\textbf{Количество публикаций} & \\textbf{Публикаций первым автором} \\\\\n\\hline\n"
    
    for year in sorted(stats['by_year'].keys()):
        count = stats['by_year'][year]
        first_author_count = stats['first_author_by_year'].get(year, 0)
        year_table += f"{year} & {count} & {first_author_count} \\\\\n\\hline\n"
    
    year_table += "\\end{tabular}\n\\end{table}"
    
    # Top journals
    journals_list = "\\begin{itemize}\n"
    for journal, count in list(stats['top_journals'].items())[:6]:
        journals_list += f"\\item \\textbf{{{journal}}} - {count} публикаций\n"
    journals_list += "\\end{itemize}"
    
    # Research areas
    areas_list = "\\begin{itemize}\n"
    area_names = {
        'control_theory': 'Теория управления и автоматизация',
        'machine_learning': 'Машинное обучение и искусственный интеллект',
        'agriculture': 'Сельскохозяйственная робототехника',
        'optimization': 'Оптимизация и алгоритмы',
        'energy': 'Энергетические системы'
    }
    
    for area, count in stats['research_areas'].items():
        if count > 0:
            areas_list += f"\\item \\textbf{{{area_names[area]}}} - {count} публикаций\n"
    areas_list += "\\end{itemize}"
    
    return {
        'basic_stats': basic_stats,
        'citation_stats': citation_stats,
        'year_table': year_table,
        'journals_list': journals_list,
        'areas_list': areas_list
    }

def main():
    bibtex_file = 'central uni grant/my_bib.bib'
    
    print("Analyzing publication statistics...")
    publications = parse_bibtex_file(bibtex_file)
    
    print(f"Found {len(publications)} publications")
    
    stats = analyze_publications(publications)
    
    print("\n=== PUBLICATION STATISTICS ===")
    print(f"Total publications: {stats['total_publications']}")
    print(f"First author publications: {stats['first_author_publications']}")
    print(f"Year range: {stats['year_range']}")
    print(f"Average per year: {stats['avg_per_year']}")
    
    print("\n=== PUBLICATIONS BY YEAR ===")
    for year in sorted(stats['by_year'].keys()):
        count = stats['by_year'][year]
        first_author_count = stats['first_author_by_year'].get(year, 0)
        print(f"{year}: {count} total, {first_author_count} first author")
    
    print("\n=== TOP JOURNALS ===")
    for journal, count in list(stats['top_journals'].items())[:6]:
        print(f"{journal}: {count} publications")
    
    print("\n=== RESEARCH AREAS ===")
    for area, count in stats['research_areas'].items():
        if count > 0:
            print(f"{area}: {count} publications")
    
    # Generate LaTeX tables
    latex_tables = generate_latex_tables(stats)
    
    # Save to file
    with open('publication_stats_latex.txt', 'w', encoding='utf-8') as f:
        f.write("=== BASIC STATISTICS TABLE ===\n")
        f.write(latex_tables['basic_stats'])
        f.write("\n\n=== CITATION STATISTICS TABLE ===\n")
        f.write(latex_tables['citation_stats'])
        f.write("\n\n=== YEARLY STATISTICS TABLE ===\n")
        f.write(latex_tables['year_table'])
        f.write("\n\n=== TOP JOURNALS LIST ===\n")
        f.write(latex_tables['journals_list'])
        f.write("\n\n=== RESEARCH AREAS LIST ===\n")
        f.write(latex_tables['areas_list'])
    
    print(f"\nLaTeX tables saved to publication_stats_latex.txt")
    
    # Save detailed stats to JSON
    with open('publication_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print("Detailed statistics saved to publication_stats.json")

if __name__ == "__main__":
    main()
