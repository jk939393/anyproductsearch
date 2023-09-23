import requests
from bs4 import BeautifulSoup
import requests
import random

import user_agents

UsrAgent = user_agents.USER_AGENTS

def scrape_content(urls):
    results = []

    for url in urls:
        headers = {
            "User-Agent": random.choice(UsrAgent)
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Try to get the regular price first
            price_div = soup.select_one('.product-intro__head-mainprice .original.from span')

            # If regular price is not found, try to get the discount price
            if not price_div:
                price_div = soup.select_one('.discount.from span')

            price = price_div.text if price_div else "Price content not found!"

            image_div = soup.select_one('.crop-image-container')
            image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"

            results.append((price, image_url))


        except requests.RequestException as e:
            print(f"Error fetching the content for {url}: {e}")
            results.append(("Error", "Error"))

    return results


# Test the function
urls = ["https://us.shein.com/SHEIN-EZwear-High-Waist-Flare-Leg-Pants-p-11805842-cat-1740.html?mallCode=1"]
scraped_results = scrape_content(urls)

for url, (price, image_url) in zip(urls, scraped_results):
    print(f"URL: {url}")
    print(f"Price: {price}")
    print(f"Image URL: {image_url}")
    print("-" * 50)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_content(urls)