import logging
import time
from bs4 import BeautifulSoup, SoupStrainer
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

HEADERS = {
    'Host': 'www.uschess.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
}
BASE_URL = 'https://www.uschess.org/index.php/Chess-Life-Magazine-pgn-game-files/?orderby=4&page='
CHROME_PATH = r"<Path To Chrome Executable>"
CHROME_DRIVER_PATH = r"<Path To Webdriver Executable>"
DOWNLOAD_DIR = ""

def setup_logging():
    logger = logging.getLogger("selenium")
    logger.setLevel(logging.WARNING)
    file_handler = logging.FileHandler('selenium.log')
    formatter = logging.Formatter("%(asctime)s %(levelname)s Selenium -> %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logging()
session = requests.Session()

def scrape_page(page_number):
    links = []
    url = BASE_URL + str(page_number)
    response = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml', parse_only=SoupStrainer('a'))
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and href.startswith('https://www.uschess.org/index.php/Start-download'):
            links.append(href)
    logger.info(f'[+] Parsing page {page_number}, {len(links)} links found!')
    return links

def scrape_all_pages(start_page, end_page):
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(scrape_page, page) for page in range(start_page, end_page + 1)]
        all_links = []
        for future in futures:
            all_links.extend(future.result())
    return all_links


options = Options()
options.binary_location = CHROME_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")
prefs = {
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': False,
    'safebrowsing.disable_download_protection': True
}
if DOWNLOAD_DIR:
    prefs['download.default_directory'] = DOWNLOAD_DIR
    prefs['savefile.default_directory'] = DOWNLOAD_DIR

options.add_experimental_option('prefs', prefs)
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

def download_files(links):
   for link in links:
       try:
           driver.get(link)
           time.sleep(0.5)
       except Exception as e:
           logger.error(f"Error downloading file from {link}: {e}")

if __name__ == "__main__":
    all_links = scrape_all_pages(1, 20)
    download_files(all_links)
    driver.close()
    driver.quit()
