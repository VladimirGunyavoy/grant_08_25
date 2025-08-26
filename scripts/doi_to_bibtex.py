#!/usr/bin/env python3
"""
Flexible script to convert DOIs to BibTeX entries
Usage: python3 doi_to_bibtex.py [DOI1 DOI2 ...] or python3 doi_to_bibtex.py --file doi_list.txt
"""

import requests
import time
import re
import json
import sys
import argparse
from urllib.parse import quote_plus

def get_bibtex_from_doi(doi):
    """Get BibTeX entry from DOI using CrossRef API"""
    try:
        # Clean the DOI
        doi = doi.strip()
        if not doi:
            return None
        
        print(f"Fetching metadata for DOI: {doi}")
        
        # Use CrossRef API to get metadata
        url = f"https://api.crossref.org/works/{doi}"
        headers = {
            'User-Agent': 'BibTeX-Generator/1.0 (mailto:user@example.com)',
            'Accept': 'application/vnd.citationstyles.csl+json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        work = data['message']
        
        # Extract metadata
        title = work.get('title', [''])[0] if work.get('title') else ''
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
        
        # Get journal information
        journal = work.get('container-title', [''])[0] if work.get('container-title') else ''
        
        # Get year
        year = None
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
                'publisher': publisher
            }
        }
        
    except Exception as e:
        print(f"Error getting BibTeX for DOI {doi}: {e}")
        return None

def read_dois_from_file(filename):
    """Read DOIs from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        dois = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                dois.append(line)
        
        return dois
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return []

def process_doi_list(doi_list):
    """Process a list of DOIs and generate BibTeX entries"""
    results = []
    failed_dois = []
    
    print(f"Processing {len(doi_list)} DOIs...")
    print("=" * 50)
    
    for i, doi in enumerate(doi_list, 1):
        print(f"[{i}/{len(doi_list)}] Processing: {doi}")
        
        result = get_bibtex_from_doi(doi)
        if result:
            results.append(result)
            metadata = result['metadata']
            print(f"  ✓ Success: {metadata['title'][:60]}...")
            print(f"     Authors: {', '.join(metadata['authors'][:3])}{'...' if len(metadata['authors']) > 3 else ''}")
            print(f"     Journal: {metadata['journal']} ({metadata['year']})")
        else:
            failed_dois.append(doi)
            print(f"  ✗ Failed to fetch metadata")
        
        print()
        
        # Be respectful to the API
        if i < len(doi_list):
            time.sleep(1)
    
    return results, failed_dois

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

def main():
    parser = argparse.ArgumentParser(description='Convert DOIs to BibTeX entries')
    parser.add_argument('dois', nargs='*', help='DOIs to convert')
    parser.add_argument('--file', '-f', help='File containing DOIs (one per line)')
    parser.add_argument('--output', '-o', default='central uni grant/my_bib.bib', help='Output BibTeX file')
    parser.add_argument('--metadata', '-m', help='Output metadata JSON file')
    
    args = parser.parse_args()
    
    # Get DOIs from arguments or file
    doi_list = []
    
    if args.file:
        doi_list = read_dois_from_file(args.file)
        if not doi_list:
            print(f"No DOIs found in file {args.file}")
            return
    elif args.dois:
        doi_list = args.dois
    else:
        print("Please provide DOIs as arguments or specify a file with --file")
        print("Example: python3 doi_to_bibtex.py 10.1016/j.automatica.2020.109123")
        print("Example: python3 doi_to_bibtex.py --file doi_list.txt")
        return
    
    print("DOI to BibTeX Converter")
    print("=" * 40)
    print(f"Input: {len(doi_list)} DOIs")
    print(f"Output: {args.output}")
    if args.metadata:
        print(f"Metadata: {args.metadata}")
    print()
    
    # Process DOIs
    results, failed_dois = process_doi_list(doi_list)
    
    # Save results
    if results:
        save_bibtex_file(results, args.output)
        if args.metadata:
            save_metadata_file(results, args.metadata)
    
    # Print summary
    print("=" * 50)
    print(f"Summary:")
    print(f"- Successfully processed: {len(results)} DOIs")
    print(f"- Failed: {len(failed_dois)} DOIs")
    
    if failed_dois:
        print(f"\nFailed DOIs:")
        for doi in failed_dois:
            print(f"  - {doi}")
    
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
