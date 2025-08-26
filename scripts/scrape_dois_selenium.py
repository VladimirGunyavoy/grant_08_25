#!/usr/bin/env python3
"""
Script to scrape DOIs from Google Scholar profile articles using Selenium
"""

import time
import re
import json
from urllib.parse import quote_plus
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure Chrome and chromedriver are installed")
        return None

def get_all_articles_selenium(url):
    """Get all articles from Google Scholar using Selenium"""
    driver = setup_driver()
    if not driver:
        return []
    
    try:
        print("Loading Google Scholar profile...")
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(3)
        
        # Find the "Show more" button and click it repeatedly
        articles_loaded = 0
        max_attempts = 20  # Prevent infinite loop
        
        for attempt in range(max_attempts):
            try:
                # Look for the "Show more" button
                show_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "gsc_bpf_more"))
                )
                
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
                time.sleep(1)
                
                # Click the button
                show_more_button.click()
                print(f"Clicked 'Show more' button (attempt {attempt + 1})")
                
                # Wait for new articles to load
                time.sleep(3)
                
                # Count current articles
                current_articles = driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
                if len(current_articles) > articles_loaded:
                    articles_loaded = len(current_articles)
                    print(f"Now loaded {articles_loaded} articles")
                else:
                    print("No new articles loaded, might be at the end")
                    break
                    
            except TimeoutException:
                print("No more 'Show more' button found - all articles loaded")
                break
            except Exception as e:
                print(f"Error clicking 'Show more': {e}")
                break
        
        # Now extract all articles
        print("Extracting article information...")
        article_elements = driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
        
        articles = []
        for element in article_elements:
            try:
                # Get title
                title_element = element.find_element(By.CLASS_NAME, "gsc_a_at")
                title = title_element.text.strip()
                
                # Get link
                link = title_element.get_attribute("href")
                
                # Get authors and year
                try:
                    authors_element = element.find_element(By.CLASS_NAME, "gs_gray")
                    authors = authors_element.text.strip()
                except NoSuchElementException:
                    authors = ""
                
                # Try to get year
                year = None
                try:
                    year_element = element.find_element(By.CLASS_NAME, "gsc_a_h")
                    year_text = year_element.text.strip()
                    year_match = re.search(r'(\d{4})', year_text)
                    if year_match:
                        year = year_match.group(1)
                except NoSuchElementException:
                    pass
                
                articles.append({
                    'title': title,
                    'authors': authors,
                    'link': link,
                    'year': year
                })
                
            except Exception as e:
                print(f"Error extracting article: {e}")
                continue
        
        print(f"Successfully extracted {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"Error in Selenium scraping: {e}")
        return []
    finally:
        driver.quit()

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
    
    print("Scraping articles from Google Scholar profile using Selenium...")
    articles = get_all_articles_selenium(url)
    
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
    with open('found_dois_selenium.json', 'w', encoding='utf-8') as f:
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
    print(f"- Results saved to 'found_dois_selenium.json'")
    print(f"- BibTeX entries saved to 'central uni grant/my_bib.bib'")
    
    # Print summary
    print(f"\nFound DOIs:")
    for article in results:
        print(f"- {article['title']}")
        print(f"  DOI: {article['doi']}")
        print()

if __name__ == "__main__":
    main()
