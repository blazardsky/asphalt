import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_with_requests(url):
    """
    Scrape website using requests and BeautifulSoup (for static content)
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def setup_selenium():
    """
    Setup Selenium WebDriver (for dynamic content)
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-agent={HEADERS['User-Agent']}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_with_selenium(url):
    """
    Scrape website using Selenium (for dynamic content)
    """
    driver = setup_selenium()
    try:
        driver.get(url)
        time.sleep(3)  # Wait for dynamic content to load
        return driver.page_source
    except Exception as e:
        print(f"Error with Selenium: {e}")
        return None
    finally:
        driver.quit()