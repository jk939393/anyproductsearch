import requests
from bs4 import BeautifulSoup

def scrape_sizes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the sizes from the provided divs
        size_divs = soup.select('.product-intro__size-radio .product-intro__size-radio-inner')
        sizes = [div.text for div in size_divs]

        return sizes

    except requests.RequestException as e:
        print(f"Error fetching the content for {url}: {e}")
        return []

# Test the function
url = "https://us.shein.com/SHEIN-EZwear-High-Waist-Flare-Leg-Pants-p-11805842-cat-1740.html?mallCode=1"
sizes = scrape_sizes(url)

print(f"Sizes available for {url}:")
for size in sizes:
    print(size)
