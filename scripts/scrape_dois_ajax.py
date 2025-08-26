#!/usr/bin/env python3
"""
Script to scrape DOIs from Google Scholar profile articles using AJAX requests
"""

import requests
import time
import re
import json
from urllib.parse import quote_plus

def get_all_articles_ajax(url):
    """Get all articles from Google Scholar using AJAX requests"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://scholar.google.com/',
    }
    
    try:
        # Extract user ID from URL
        user_id = None
        match = re.search(r'user=([^&]+)', url)
        if match:
            user_id = match.group(1)
        
        if not user_id:
            print("Could not extract user ID from URL")
            return []
        
        print(f"Using user ID: {user_id}")
        
        # Try to get all articles by making multiple requests
        all_articles = []
        start = 0
        batch_size = 20
        
        # Try different approaches to get all articles
        for attempt in range(10):  # Try up to 10 batches
            print(f"Attempting to load batch {attempt + 1} (start={start})...")
            
            # Method 1: Try the standard pagination URL
            ajax_url = f"https://scholar.google.com/citations?user={user_id}&hl=ru&oi=ao&cstart={start}&pagesize={batch_size}"
            
            try:
                response = requests.get(ajax_url, headers=headers, timeout=15)
                response.raise_for_status()
                
                # Check if we got HTML content
                if 'gsc_a_tr' in response.text:
                    # Parse the HTML to extract articles
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    article_elements = soup.find_all('tr', class_='gsc_a_tr')
                    
                    if not article_elements:
                        print("No articles found in this batch")
                        break
                    
                    batch_articles = []
                    for element in article_elements:
                        title_element = element.find('a', class_='gsc_a_at')
                        if title_element:
                            title = title_element.get_text(strip=True)
                            link = title_element.get('href', '')
                            if link.startswith('/'):
                                link = 'https://scholar.google.com' + link
                            
                            # Get authors
                            authors_element = element.find('div', class_='gs_gray')
                            authors = authors_element.get_text(strip=True) if authors_element else ""
                            
                            # Get year
                            year = None
                            year_element = element.find('span', class_='gsc_a_h')
                            if year_element:
                                year_text = year_element.get_text(strip=True)
                                year_match = re.search(r'(\d{4})', year_text)
                                if year_match:
                                    year = year_match.group(1)
                            
                            batch_articles.append({
                                'title': title,
                                'authors': authors,
                                'link': link,
                                'year': year
                            })
                    
                    # Check if we got new articles
                    new_articles = [a for a in batch_articles if a not in all_articles]
                    if new_articles:
                        all_articles.extend(new_articles)
                        print(f"Added {len(new_articles)} new articles (total: {len(all_articles)})")
                    else:
                        print("No new articles found, might be at the end")
                        break
                    
                    start += batch_size
                    time.sleep(2)  # Be respectful
                    
                else:
                    print("No article data found in response")
                    break
                    
            except Exception as e:
                print(f"Error loading batch {attempt + 1}: {e}")
                break
        
        print(f"Total articles collected: {len(all_articles)}")
        return all_articles
        
    except Exception as e:
        print(f"Error in AJAX scraping: {e}")
        return []

def search_doi_by_title(title):
    """Search for DOI using article title via CrossRef API"""
    try:
        # Clean the title for search
        clean_title = re.sub(r'[^\w\s]', '', title).strip()
        search_query = quote_plus(clean_title)
        
        # Use CrossRef API
        url = f"https://api.crossref.org/works?query={search_query}&rows=5"
        headers = {
            'User-Agent': 'DOI-Scraper/1.0 (mailto:user@example.com)'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['message']['items']:
            # Find the best match
            for item in data['message']['items']:
                item_title = item.get('title', [''])[0] if item.get('title') else ''
                if item_title and similar_titles(title, item_title):
                    return item.get('DOI', '')
        
        return ""
    
    except Exception as e:
        print(f"Error searching DOI for '{title}': {e}")
        return ""

def similar_titles(title1, title2, threshold=0.7):
    """Check if two titles are similar using simple string matching"""
    title1_clean = re.sub(r'[^\w\s]', '', title1.lower())
    title2_clean = re.sub(r'[^\w\s]', '', title2.lower())
    
    # Simple similarity check
    words1 = set(title1_clean.split())
    words2 = set(title2_clean.split())
    
    if not words1 or not words2:
        return False
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    similarity = len(intersection) / len(union)
    return similarity >= threshold

def create_bibtex_entry(title, authors, doi, year=None):
    """Create a BibTeX entry"""
    # Generate a key from the title
    key = re.sub(r'[^\w\s]', '', title.lower())
    key = re.sub(r'\s+', '_', key)[:30]
    
    bibtex = f"""@article{{{key},
  title = {{{title}}},
  author = {{{authors}}},
  doi = {{{doi}}},
"""
    
    if year:
        bibtex += f"  year = {{{year}}},\n"
    
    bibtex += "}\n\n"
    return bibtex

def main():
    url = "https://scholar.google.com/citations?user=bROxyNoAAAAJ&hl=ru&oi=ao"
    
    print("Scraping articles from Google Scholar profile using AJAX...")
    articles = get_all_articles_ajax(url)
    
    if not articles:
        print("No articles found or error occurred.")
        return
    
    print(f"Found {len(articles)} articles. Searching for DOIs...")
    
    results = []
    for i, article in enumerate(articles, 1):
        print(f"Processing {i}/{len(articles)}: {article['title'][:50]}...")
        
        doi = search_doi_by_title(article['title'])
        if doi:
            article['doi'] = doi
            results.append(article)
            print(f"  ✓ Found DOI: {doi}")
        else:
            print(f"  ✗ No DOI found")
        
        # Be respectful to the API
        time.sleep(1)
    
    # Save results to file
    with open('found_dois_ajax.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Create BibTeX file
    bibtex_content = ""
    for article in results:
        bibtex_content += create_bibtex_entry(
            article['title'],
            article['authors'],
            article['doi'],
            article.get('year')
        )
    
    with open('central uni grant/my_bib.bib', 'w', encoding='utf-8') as f:
        f.write(bibtex_content)
    
    print(f"\nResults:")
    print(f"- Found DOIs for {len(results)} out of {len(articles)} articles")
    print(f"- Results saved to 'found_dois_ajax.json'")
    print(f"- BibTeX entries saved to 'central uni grant/my_bib.bib'")
    
    # Print summary
    print(f"\nFound DOIs:")
    for article in results:
        print(f"- {article['title']}")
        print(f"  DOI: {article['doi']}")
        print()

if __name__ == "__main__":
    main()
