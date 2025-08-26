#!/usr/bin/env python3
"""
Script to scrape DOIs from Google Scholar profile articles
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote_plus
import json

def get_google_scholar_articles(url):
    """Scrape article information from Google Scholar profile with pagination"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # First, get the initial page to extract user ID and other parameters
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract user ID from the page
        user_id = None
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'user=' in script.string:
                match = re.search(r'user=([^&"]+)', script.string)
                if match:
                    user_id = match.group(1)
                    break
        
        if not user_id:
            # Fallback: extract from URL
            match = re.search(r'user=([^&]+)', url)
            if match:
                user_id = match.group(1)
        
        if not user_id:
            print("Could not extract user ID")
            return []
        
        print(f"Found user ID: {user_id}")
        
        # Get total number of articles
        total_articles = 0
        total_element = soup.find('span', class_='gsc_rsb_a_p')
        if total_element:
            total_text = total_element.get_text()
            match = re.search(r'(\d+)', total_text)
            if match:
                total_articles = int(match.group(1))
        
        print(f"Total articles reported: {total_articles}")
        
        # Collect articles from all pages
        all_articles = []
        start = 0
        batch_size = 20  # Google Scholar loads 20 articles per batch
        
        while True:
            print(f"Loading articles {start}-{start + batch_size}...")
            
            # Construct the AJAX URL for loading more articles
            ajax_url = f"https://scholar.google.com/citations?user={user_id}&hl=ru&oi=ao&cstart={start}&pagesize={batch_size}"
            
            try:
                response = requests.get(ajax_url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all article entries
                article_elements = soup.find_all('tr', class_='gsc_a_tr')
                
                if not article_elements:
                    print("No more articles found")
                    break
                
                page_articles = []
                for element in article_elements:
                    title_element = element.find('a', class_='gsc_a_at')
                    if title_element:
                        title = title_element.get_text(strip=True)
                        link = title_element.get('href', '')
                        if link.startswith('/'):
                            link = 'https://scholar.google.com' + link
                        
                        # Try to get authors and year
                        authors_element = element.find('div', class_='gs_gray')
                        authors = authors_element.get_text(strip=True) if authors_element else ""
                        
                        # Try to get year
                        year = None
                        year_element = element.find('span', class_='gsc_a_h')
                        if year_element:
                            year_text = year_element.get_text(strip=True)
                            year_match = re.search(r'(\d{4})', year_text)
                            if year_match:
                                year = year_match.group(1)
                        
                        page_articles.append({
                            'title': title,
                            'authors': authors,
                            'link': link,
                            'year': year
                        })
                
                all_articles.extend(page_articles)
                print(f"Found {len(page_articles)} articles on this page")
                
                # Check if we've loaded all articles
                if len(page_articles) < batch_size or len(all_articles) >= total_articles:
                    break
                
                start += batch_size
                
                # Be respectful to the server
                time.sleep(2)
                
            except Exception as e:
                print(f"Error loading page {start}: {e}")
                break
        
        print(f"Total articles collected: {len(all_articles)}")
        return all_articles
    
    except Exception as e:
        print(f"Error scraping Google Scholar: {e}")
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
    
    print("Scraping articles from Google Scholar profile...")
    articles = get_google_scholar_articles(url)
    
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
    with open('found_dois.json', 'w', encoding='utf-8') as f:
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
    print(f"- Results saved to 'found_dois.json'")
    print(f"- BibTeX entries saved to 'central uni grant/my_bib.bib'")
    
    # Print summary
    print(f"\nFound DOIs:")
    for article in results:
        print(f"- {article['title']}")
        print(f"  DOI: {article['doi']}")
        print()

if __name__ == "__main__":
    main()
