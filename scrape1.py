from bs4 import BeautifulSoup
import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import logging
import user_agents_file

logging.basicConfig(level=logging.DEBUG)
UsrAgent = user_agents_file.USER_AGENTS

def scrape_single_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    size_divs = soup.select('.product-intro__size-radio .product-intro__size-radio-inner')
    sizes = [div.text for div in size_divs]

    price_div = soup.select_one('.product-intro__head-mainprice .original.from span')
    if not price_div:
        price_div = soup.select_one('.discount.from span')
    price = price_div.text if price_div else "Price content not found!"

    image_div = soup.select_one('.crop-image-container')
    image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"

    driver.quit()

    return (price, image_url, sizes)

def scrape_content(urls):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_single_url, urls))
    return results


# Test the function
urls = ["https://us.shein.com/SHEIN-EZwear-High-Waist-Flare-Leg-Pants-p-11805842-cat-1740.html?mallCode=1"]
scraped_results = scrape_content(urls)

for url, (price, image_url, sizes) in zip(urls, scraped_results):
    logging.info(f"URL: {url}")
    logging.info(f"Price: {price}")
    logging.info(f"Image URL: {image_url}")
    logging.info(f"Sizes: {', '.join(sizes)}")

if __name__ == '__main__':
    scrape_content(urls)
