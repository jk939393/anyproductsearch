import requests
from bs4 import BeautifulSoup


def scrape_content():
    # Define the URL
    url = "https://us.shein.com/Men-Cotton-Ripped-Moustache-Effect-Skinny-Jeans-p-10909859-cat-1987.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Make a request to the website
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the desired div and extract the content
        price_div = soup.select_one('.product-intro__head-mainprice .original.from span')
        price = price_div.text if price_div else "Price content not found!"

        image_div = soup.select_one('.crop-image-container')
        image_url = image_div['data-before-crop-src'] if image_div else "Image content not found!"

        return price, image_url

    except requests.RequestException as e:
        print(f"Error fetching the content: {e}")
        return None, None


# Test the function
price, image_url = scrape_content()
print(price)
print(image_url)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_content()