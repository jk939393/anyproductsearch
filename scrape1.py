import requests
from bs4 import BeautifulSoup


def scrape_content(urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    results = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            price_div = soup.select_one('.product-intro__head-mainprice .original.from span')
            price = price_div.text if price_div else "Price content not found!"

            image_div = soup.select_one('.crop-image-container')
            image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"

            results.append((price, image_url))

        except requests.RequestException as e:
            print(f"Error fetching the content for {url}: {e}")
            results.append(("Error", "Error"))

    return results


# Test the function
urls = ["https://us.shein.com/Men-Cotton-Ripped-Moustache-Effect-Skinny-Jeans-p-10909859-cat-1987.html"]
scraped_results = scrape_content(urls)

for url, (price, image_url) in zip(urls, scraped_results):
    print(f"URL: {url}")
    print(f"Price: {price}")
    print(f"Image URL: {image_url}")
    print("-" * 50)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_content(urls)