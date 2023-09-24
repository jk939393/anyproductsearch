from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pyshorteners


logging.basicConfig(level=logging.DEBUG)


class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if chromedriver_path:
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.shortener = pyshorteners.Shortener()

    def scrape_content(self, urls):
        results = []
        for url in urls:
            self.driver.get(url)

            # Fetch page source and parse it with BeautifulSoup
            page_source = self.driver.page_source
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

            # Shorten the image URL
            short_image_url = self.shortener.tinyurl.short(image_url)

            results.append((price, image_url, sizes))
            print(short_image_url)

        return results

    def close(self):
        self.driver.quit()
