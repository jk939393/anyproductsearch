import requests
from bs4 import BeautifulSoup

def scrape_size_number(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the size numbers from the aria-label attribute
        size_divs = soup.select('.product-intro__size-radio[aria-label]')
        size_numbers = [div['aria-label'].split()[0] for div in size_divs]

        return size_numbers

    except requests.RequestException as e:
        print(f"Error fetching the content for {url}: {e}")
        return []

# Test the function
url = "https://us.shein.com/SHEIN-EZwear-High-Waist-Flare-Leg-Pants-p-11805842-cat-1740.html?mallCode=1"
size_numbers = scrape_size_number(url)

print(f"Size numbers available for {url}:")
for size_number in size_numbers:
    print(size_number)





