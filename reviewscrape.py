from bs4 import BeautifulSoup


def extract_rating_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    rating_div = soup.select_one('.rate-num')

    if rating_div:
        rating = rating_div.text.strip()
        return rating
    else:
        return None


# Specify the local file path
file_path = 'C:/Users/jkras/Downloads/SHEIN Clasi Plus Plaid Print Leggings _ SHEIN USA.html'

rating = extract_rating_from_file(file_path)

if rating:
    print(f"Extracted rating: {rating}")
else:
    print(f"Could not extract rating from the provided file.")








