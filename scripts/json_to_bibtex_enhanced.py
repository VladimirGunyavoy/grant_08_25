#!/usr/bin/env python3
"""
Enhanced script to read DOIs from JSON file and generate BibTeX entries
- Filters out preprints
- Includes citation counts
- Uses year from JSON file
"""

import json
import requests
import time
import re
import argparse
from urllib.parse import quote_plus

def is_preprint(doi):
    """Check if DOI is a preprint"""
    preprint_patterns = [
        r'arxiv\.org',
        r'bioarxiv\.org',
        r'medarxiv\.org',
        r'chemrxiv\.org',
        r'psyarxiv\.org',
        r'socarxiv\.org',
        r'osf\.io',
        r'preprints\.org',
        r'researchsquare\.com',
        r'biorxiv\.org'
    ]
    
    doi_lower = doi.lower()
    for pattern in preprint_patterns:
        if re.search(pattern, doi_lower):
            return True
    return False

def get_bibtex_from_doi(doi, year_from_json=None, title_from_json=None, authors_from_json=None):
    """Get BibTeX entry from DOI using CrossRef API"""
    try:
        # Clean the DOI
        doi = doi.strip()
        if not doi:
            return None
        
        # Skip preprints
        if is_preprint(doi):
            print(f"Skipping preprint: {doi}")
            return None
        
        print(f"Fetching metadata for DOI: {doi}")
        
        # Use CrossRef API to get metadata
        url = f"https://api.crossref.org/works/{doi}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        work = data['message']
        
        # Extract metadata
        title = work.get('title', [''])[0] if work.get('title') else title_from_json or ''
        authors = []
        
        if work.get('author'):
            for author in work['author']:
                given = author.get('given', '')
                family = author.get('family', '')
                if given and family:
                    authors.append(f"{given} {family}")
                elif family:
                    authors.append(family)
                elif given:
                    authors.append(given)
        elif authors_from_json:
            # Use authors from JSON if CrossRef doesn't have them
            authors = [author.strip() for author in authors_from_json.split(',')]
        
        # Get journal information
        journal = work.get('container-title', [''])[0] if work.get('container-title') else ''
        
        # Get year - prefer from JSON, fallback to CrossRef
        year = year_from_json
        if not year:
            if work.get('published-print'):
                year = work['published-print']['date-parts'][0][0]
            elif work.get('published-online'):
                year = work['published-online']['date-parts'][0][0]
            elif work.get('created'):
                year = work['created']['date-parts'][0][0]
        
        # Get volume and issue
        volume = work.get('volume', '')
        issue = work.get('issue', '')
        
        # Get pages
        pages = ''
        if work.get('page'):
            pages = work['page']
        
        # Get publisher
        publisher = work.get('publisher', '')
        
        # Generate BibTeX key
        if authors:
            first_author = authors[0].split()[-1]  # Last name of first author
        else:
            first_author = "Unknown"
        
        if year:
            key = f"{first_author}{year}"
        else:
            key = f"{first_author}Unknown"
        
        # Create BibTeX entry
        bibtex = f"""@article{{{key},
  title = {{{title}}},
  author = {{{' and '.join(authors)}}},
  journal = {{{journal}}},
  year = {{{year}}},
  doi = {{{doi}}},
"""
        
        if volume:
            bibtex += f"  volume = {{{volume}}},\n"
        
        if issue:
            bibtex += f"  number = {{{issue}}},\n"
        
        if pages:
            bibtex += f"  pages = {{{pages}}},\n"
        
        if publisher:
            bibtex += f"  publisher = {{{publisher}}},\n"
        
        # Add citation count field (empty for now, can be filled manually)
        bibtex += f"  citations = {{}},\n"
        
        bibtex += "}\n\n"
        
        return {
            'bibtex': bibtex,
            'metadata': {
                'title': title,
                'authors': authors,
                'journal': journal,
                'year': year,
                'doi': doi,
                'volume': volume,
                'issue': issue,
                'pages': pages,
                'publisher': publisher,
                'citations': None  # Placeholder for citation count
            }
        }
        
    except Exception as e:
        print(f"Error getting BibTeX for DOI {doi}: {e}")
        return None

def read_articles_from_json(filename):
    """Read articles from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        articles = []
        for item in data:
            if isinstance(item, dict) and 'doi' in item:
                doi = item['doi']
                if doi and doi.strip():
                    articles.append({
                        'doi': doi.strip(),
                        'title': item.get('title', ''),
                        'authors': item.get('authors', ''),
                        'year': item.get('year', ''),
                        'link': item.get('link', '')
                    })
        
        return articles
    except Exception as e:
        print(f"Error reading JSON file {filename}: {e}")
        return []

def process_articles(articles):
    """Process articles and generate BibTeX entries"""
    results = []
    failed_dois = []
    skipped_preprints = []
    
    print(f"Processing {len(articles)} articles...")
    print("=" * 50)
    
    for i, article in enumerate(articles, 1):
        doi = article['doi']
        print(f"[{i}/{len(articles)}] Processing: {doi}")
        
        # Skip preprints
        if is_preprint(doi):
            skipped_preprints.append(article)
            print(f"  ⚠ Skipped preprint")
            continue
        
        result = get_bibtex_from_doi(
            doi, 
            year_from_json=article.get('year'),
            title_from_json=article.get('title'),
            authors_from_json=article.get('authors')
        )
        
        if result:
            results.append(result)
            metadata = result['metadata']
            print(f"  ✓ Success: {metadata['title'][:60]}...")
            print(f"     Authors: {', '.join(metadata['authors'][:3])}{'...' if len(metadata['authors']) > 3 else ''}")
            print(f"     Journal: {metadata['journal']} ({metadata['year']})")
        else:
            failed_dois.append(article)
            print(f"  ✗ Failed to fetch metadata")
        
        print()
        
        # Be respectful to the API
        if i < len(articles):
            time.sleep(1)
    
    return results, failed_dois, skipped_preprints

def save_bibtex_file(results, filename):
    """Save BibTeX entries to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result['bibtex'])
    
    print(f"BibTeX entries saved to {filename}")

def save_metadata_file(results, filename):
    """Save metadata to JSON file"""
    metadata_list = [result['metadata'] for result in results]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    
    print(f"Metadata saved to {filename}")

def save_failed_dois(failed_dois, filename):
    """Save failed DOIs to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for article in failed_dois:
            f.write(f"{article['doi']}\t{article.get('title', '')}\n")
    
    print(f"Failed DOIs saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Convert DOIs from JSON file to BibTeX entries')
    parser.add_argument('--input', '-i', default='found_dois_ajax.json', help='Input JSON file with articles')
    parser.add_argument('--output', '-o', default='central uni grant/my_bib.bib', help='Output BibTeX file')
    parser.add_argument('--metadata', '-m', help='Output metadata JSON file')
    parser.add_argument('--failed', '-f', help='Output file for failed DOIs')
    
    args = parser.parse_args()
    
    print("Enhanced JSON to BibTeX Converter")
    print("=" * 40)
    print(f"Input JSON: {args.input}")
    print(f"Output BibTeX: {args.output}")
    if args.metadata:
        print(f"Output metadata: {args.metadata}")
    if args.failed:
        print(f"Failed DOIs: {args.failed}")
    print()
    
    # Read articles from JSON file
    articles = read_articles_from_json(args.input)
    
    if not articles:
        print(f"No articles found in {args.input}")
        return
    
    print(f"Found {len(articles)} articles in {args.input}")
    print()
    
    # Process articles
    results, failed_dois, skipped_preprints = process_articles(articles)
    
    # Save results
    if results:
        save_bibtex_file(results, args.output)
        if args.metadata:
            save_metadata_file(results, args.metadata)
    
    if failed_dois and args.failed:
        save_failed_dois(failed_dois, args.failed)
    
    # Print summary
    print("=" * 50)
    print(f"Summary:")
    print(f"- Successfully processed: {len(results)} articles")
    print(f"- Failed: {len(failed_dois)} articles")
    print(f"- Skipped preprints: {len(skipped_preprints)} articles")
    
    if skipped_preprints:
        print(f"\nSkipped preprints:")
        for article in skipped_preprints:
            print(f"  - {article['doi']} ({article.get('title', '')[:50]}...)")
    
    if failed_dois:
        print(f"\nFailed DOIs:")
        for article in failed_dois:
            print(f"  - {article['doi']} ({article.get('title', '')[:50]}...)")
    
    if results:
        print(f"\nGenerated BibTeX entries:")
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            print(f"{i}. {metadata['title']}")
            print(f"   Authors: {', '.join(metadata['authors'])}")
            print(f"   Journal: {metadata['journal']} ({metadata['year']})")
            print(f"   DOI: {metadata['doi']}")
            print()

if __name__ == "__main__":
    main()
