import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)

def scrape_content(urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    results = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            logging.debug(f"Status code for {url}: {response.status_code}")
            logging.debug(f"Content Snippet for {url}: {response.content[:1000].decode('utf-8')}")

            soup = BeautifulSoup(response.content, 'html.parser')

            price_div = soup.select_one('.product-intro__head-mainprice .original.from span')
            if not price_div:
                price_div = soup.select_one('.discount.from span')
            price = price_div.text if price_div else "Price content not found!"
            logging.debug(f"Price div content for {url}: {price_div}")

            image_div = soup.select_one('.crop-image-container')
            image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"
            logging.debug(f"Image div content for {url}: {image_div}")

            results.append((price, image_url))

        except requests.RequestException as e:
            logging.error(f"Error fetching the content for {url}: {e}")
            results.append(("Error", "Error"))

    return results

# Test the function
urls = ["https://us.shein.com/SHEIN-EZwear-High-Waist-Flare-Leg-Pants-p-11805842-cat-1740.html?mallCode=1"]
scraped_results = scrape_content(urls)

for url, (price, image_url) in zip(urls, scraped_results):
    logging.info(f"URL: {url}")
    logging.info(f"Price: {price}")
    logging.info(f"Image URL: {image_url}")

if __name__ == '__main__':
    scrape_content(urls)
