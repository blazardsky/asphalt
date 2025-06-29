import pandas as pd
from urllib.parse import urlparse
import json, os

from app.scraper import scrape_with_requests

def load_selectors(file_path):
    """
    Load selectors from the external file
    file_path: path to the selectors.json file
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: selectors.json file not found!")
        return None
    except json.JSONDecodeError:
        print("Error: selectors.json contains invalid JSON!")
        return None

def check_url(url):
    """
    Check if the URL is valid
    """
    if not url.strip():
        print("URL is not set")
        return
    if not url.startswith("http"):
        url = "https://" + url
        print(f"I'm going to scan: {url}")
    return url

def get_domain(url):
    """
    Extract domain from URL
    """
    parsed_uri = urlparse(url)
    return parsed_uri.netloc

def get_article_full_url(url, link):
    """
    Get the full URL of the article
    """
    if not link.startswith('http'):
        link = f"https://{get_domain(url)}{link}"
    return link

def extract_article_links(url, selectors):
    """
    Extract article links from the website
    """
    selector = selectors['blog']
    soup = scrape_with_requests(url)
    link_elements = soup.select(selector['link'])
    print(f"Found {len(link_elements)} link elements")
    
    articles_links = []
    for link_elem in link_elements:
        link = get_article_full_url(url, link_elem['href'])
        articles_links.append(link)
    
    return articles_links

def extract_article_data(url, selectors): # url, soup, selectors
    """
    Extract article data based on site type
    """
    
    selector = selectors['single']
    soup = scrape_with_requests(url)
    
    try:
        # Extract title
        title_elem = soup.select_one(selector['title'])
        title = title_elem.get_text(strip=True) if title_elem else ''
        
        # Extract content
        content_elem = soup.select_one(selector['content'])
        if content_elem:
            # Get all child elements that match the content tags
            content_elems = content_elem.find_all(selector['content_tags'])
            content = ' '.join([tag.get_text(strip=True) for tag in content_elems if tag.get_text(strip=True)])
        else:
            content = 'N/A'
        
        # Extract date
        date_elem = soup.select_one(selector['date'])
        date = date_elem.get_text(strip=True) if date_elem else ''
    
        if title:
            return {
                'title': title,
                'content': content,
                'date': date,
            }
        
    except Exception as e:
        print(f"Error extracting article data: {e}")
    


def save_to_csv(data, filename):
    """
    Save scraped data to CSV
    """
    if not data:
        print("No data to save!")
        return
        
    path = os.path.join(os.getcwd(), "output", filename)
    df = pd.DataFrame(data)
    df.to_csv(path, index=False, encoding='utf-8')
    print(f"Data saved to {path}")