from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
<<<<<<< HEAD
import os
import pyshorteners


logging.basicConfig(level=logging.DEBUG)


=======
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
import pyshorteners

logging.basicConfig(level=logging.DEBUG)

>>>>>>> 6f25d45ff65a64818deb384f323bf262e0262a45
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

<<<<<<< HEAD
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if chromedriver_path:
            self.driver = webdriver.Chrome(options=chrome_options)
=======
        # Set up proxy
        self.proxies = [
            "http://34.23.45.223:80",
            "socks5://70.35.199.99:52344",
            "socks4://50.7.67.212:63812",
            "http://123.205.68.113:8193",
            "http://165.16.60.245:8080",
            "http://38.156.238.94:999",
            "http://83.97.20.192:8080",
            "http://136.243.92.30:26541",
            "http://185.73.202.125:3128",
            "http://172.111.10.191:3128",
            "http://36.37.81.135:8080",
            "socks4://64.90.51.183:44074",
            "http://202.57.30.66:80",
            "http://139.162.99.100:8080"
        ]
        selected_proxy = self.select_proxy()  # Select a proxy from the list
        if selected_proxy:
            chrome_options = self.set_proxy(chrome_options, selected_proxy)

        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if chromedriver_path:
            self.driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
>>>>>>> 6f25d45ff65a64818deb384f323bf262e0262a45
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.shortener = pyshorteners.Shortener()

<<<<<<< HEAD
=======
    def select_proxy(self):
        # For simplicity, we're just picking a random proxy. You can implement more complex logic.
        import random
        return random.choice(self.proxies)

    def set_proxy(self, chrome_options, proxy):
        proxy_obj = Proxy()
        proxy_obj.proxy_type = ProxyType.MANUAL
        if "http" in proxy:
            proxy_obj.http_proxy = proxy
            proxy_obj.ssl_proxy = proxy
        elif "socks4" in proxy:
            proxy_obj.socks4_proxy = proxy
        elif "socks5" in proxy:
            proxy_obj.socks5_proxy = proxy

        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy_obj.add_to_capabilities(capabilities)

        chrome_options.merge(capabilities)

        return chrome_options

>>>>>>> 6f25d45ff65a64818deb384f323bf262e0262a45
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

<<<<<<< HEAD
            # Shorten the image URL
            short_image_url = self.shortener.tinyurl.short(image_url)
=======
            url_to_shorten = "http://Image content not found!"

            if url_to_shorten != "http://Image content not found!":
                short_image_url = self.shortener.tinyurl.short(url_to_shorten)
            else:
                short_image_url = url_to_shorten  # or any other default value you'd like
>>>>>>> 6f25d45ff65a64818deb384f323bf262e0262a45

            results.append((price, image_url, sizes))
            print(short_image_url)

        return results

    def close(self):
        self.driver.quit()
<<<<<<< HEAD
=======

# Example usage:
# scraper = Scraper()
# urls = ["http://example.com/product1", "http://example.com/product2"]
# scraper.scrape_content(urls)
# scraper.close()
>>>>>>> 6f25d45ff65a64818deb384f323bf262e0262a45
