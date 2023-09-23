from bs4 import BeautifulSoup
import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

import user_agents_file

logging.basicConfig(level=logging.DEBUG)
UsrAgent = user_agents_file.USER_AGENTS

def scrape_content(urls):
    results = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Initialize Selenium Chrome driver
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
    if chromedriver_path:
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    for url in urls:
        driver.get(url)
        #time.sleep(random.uniform(1, 5))  # Rate limiting

        # Fetch page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extracting the sizes
        size_divs = soup.select('.product-intro__size-radio .product-intro__size-radio-inner')
        sizes = [div.text for div in size_divs]

        # Extracting the price
        price_div = soup.select_one('.product-intro__head-mainprice .original.from span')
        if not price_div:
            price_div = soup.select_one('.discount.from span')
        price = price_div.text if price_div else "Price content not found!"

        # Extracting the image URL
        image_div = soup.select_one('.crop-image-container')
        image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"

        results.append((price, image_url, sizes))

    driver.quit()
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
