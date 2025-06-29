import requests
from bs4 import BeautifulSoup
import time

def extract_article_data(soup, selectors):
    """
    Extract article data
    """
    if not selectors:
        print(f"Error: No selectors found")
        return []
    
    # Debug: Check if soup is a BeautifulSoup object
    if not isinstance(soup, BeautifulSoup):
        print(f"Error: Expected BeautifulSoup object, got {type(soup)}")
        if isinstance(soup, str):
            print("Converting string to BeautifulSoup object...")
            soup = BeautifulSoup(soup, 'html.parser')
        else:
            return []
        
    articles = []
    selector = selectors['single']
    
    # Find all articles
    try:
        article_elements = soup.select(selector['article'])
        print(f"Found {len(article_elements)} article elements")
    except Exception as e:
        print(f"Error selecting articles: {e}")
        return []
    
    for article in article_elements:
        try:
            # Extract title
            title_elem = article.select_one(selector['title'])
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Extract content (first few paragraphs)
            content_elems = article.select(selector['content'])
            content = ' '.join([p.get_text(strip=True) for p in content_elems[:3]])
            
            # Extract date
            date_elem = article.select_one(selector['date'])
            date = date_elem.get_text(strip=True) if date_elem else ''
    
            
            if title:  # Only add if we found at least a title
                articles.append({
                    'title': title,
                    'content': content,
                    'date': date
                })
        except Exception as e:
            print(f"Error extracting article data: {e}")
            continue
    
    return articles

def scrape_with_requests(url):
    """
    Scrape website using requests and BeautifulSoup (for static content)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Successfully created BeautifulSoup object from requests")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def scrape_with_selenium(url):
    """
    Scrape website using Selenium (for dynamic content)
    """
    driver = setup_selenium()
    try:
        driver.get(url)
        time.sleep(3)  # Wait for dynamic content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("Successfully created BeautifulSoup object from Selenium")
        return soup
    except Exception as e:
        print(f"Error with Selenium: {e}")
        return None
    finally:
        driver.quit()

def main():
    # Load selectors first
    selectors = load_selectors()
    if not selectors:
        return
        
    url = check_url(input("Enter the URL of the blog or news website: "))
    if not url:
        return
        
    site_type = detect_site_type(url)
    print(f"Detected site type: {site_type}")
    
    # Try with requests first (faster)
    soup = scrape_with_requests(url)
    articles = []
    
    if soup:
        print(f"Type of soup object: {type(soup)}")
        articles = extract_article_data(soup, site_type, selectors)
    
    # If no articles found or requests failed, try Selenium
    if not articles:
        print("Trying with Selenium...")
        soup = scrape_with_selenium(url)
        if soup:
            print(f"Type of soup object: {type(soup)}")
            articles = extract_article_data(soup, site_type, selectors)
    
    if articles:
        print(f"Found {len(articles)} articles")
        save_to_csv(articles, 'articles.csv')
    else:
        print("No articles found!") 