from app.scraper import scrape_with_requests, scrape_with_selenium
from app.utils import load_selectors, check_url, extract_article_data, save_to_csv, extract_article_links
from bs4 import BeautifulSoup
import argparse, os
from datetime import datetime

def main():

    parser = argparse.ArgumentParser(description="Asphalt scraper.")
    parser.add_argument("url", nargs="?", help="The URL to process")
    parser.add_argument("-a", action="store_true", help="If scraping for a single (a)rticle")
    parser.add_argument("-b", action="store_true", help="If scraping for a (b)log")
    parser.add_argument("--list", type=str, help="Path to txt file with URLs")
    parser.add_argument("--selectors", type=str, help="Selectors identifier (e.g. ghost, medium, etc.)")

    args = parser.parse_args()

    # Get URLs
    urls = []
    if args.list:
        with open(args.list, "r") as f:
            urls = [line.strip() for line in f.readlines()]
    elif args.url:
        urls = [args.url]
    else:
        parser.error("No URL or --list provided.")


    # Load selectors first
    list_selectors = [f.replace('.json', '') for f in os.listdir('app/selectors')]
    selectors_url = f'app/selectors/{args.selectors}.json' if args.selectors and args.selectors in list_selectors else 'app/selectors/selectors.json'
    selectors = load_selectors(selectors_url)
    if not selectors:
        parser.error("No selectors provided. Check the selectors file.")
        

        
    site_type = 'a' if args.a else 'b' if args.b else None
    if not site_type:
        parser.error("No site type provided. Use -a for a single article or -b for a blog page.")
    
    articles_links = []
    if site_type == 'b':
        for url in urls:
            articles_links.extend(extract_article_links(url, selectors))
    else:
        articles_links = urls

    articles = []
    for link in articles_links:
        articles.append( extract_article_data( link, selectors ) )

    filename = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    print(f"Found {len(articles)} articles. Saving to {filename}...")
    save_to_csv(articles, filename)


if __name__ == "__main__":
    main() 