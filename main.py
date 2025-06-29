from app.scraper import scrape_with_requests, scrape_with_selenium
from app.utils import load_selectors, check_url, extract_article_data, save_to_csv, extract_article_links
from bs4 import BeautifulSoup

def main():
    # Load selectors first
    selectors = load_selectors('app/selectors.json')
    if not selectors:
        return
        
    url = check_url(input("Enter the URL of the blog or news website: "))
    if not url:
        return
        
    site_type = ''
    print("Select the site type:")
    while site_type not in ['a', 'b']:
        site_type = input("(a)rticle or (b)log: ")
        if site_type not in ['a', 'b']:
            print("Invalid site type. Please enter 'a' or 'b'.")
    
    articles_links = []
    if site_type == 'b':
        articles_links = extract_article_links(url, selectors)
    else:
        articles_links.append(url)

    articles = []
    for link in articles_links:
        articles.append( extract_article_data( link, selectors ) )

    filename = f"{url.replace('/', '_')}.csv"
    print(f"Found {len(articles)} articles")
    save_to_csv(articles, filename)


if __name__ == "__main__":
    print(">>> Scraper started...")
    main() 