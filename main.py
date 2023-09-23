import json

import quart
import quart_cors
from quart import request
import requests
import os
import re
import httpx
from datetime import datetime
import scrape1
#with AI suggestions most powerful AI tool # a fun and powerful product search app with ai recomenndations  #specify and rating and price for a custom AI recommendation
import urllib.parse
API_KEY = "AIzaSyBbvhM0tfQDlrI2ndRbZAN1YKBmwwStIrw"
CX = "c5242d010cb334682"
a=API_KEY
b= CX
BASE_URL = "https://www.googleapis.com/customsearch/v1/siterestrict"

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
#pubmed

@app.route("/")
async def hello():
    return "Hello, World 01 "




#with AI suggestions most powerful AI tool # a fun and powerful product search app with ai recomenndations  #specify and rating and price for a custom AI recommendation
import urllib.parse
API_KEY = "AIzaSyBbvhM0tfQDlrI2ndRbZAN1YKBmwwStIrw"
CX = "c5242d010cb334682"
a=API_KEY
b= CX
BASE_URL = "https://www.googleapis.com/customsearch/v1/siterestrict"

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
#pubmed


@app.route("/google_search/<string:query>", methods=['GET'])
async def get_google_search_results(query, page=1):
    try:
        query = f"{query} highly rated for adults"
        # Calculate the start index for pagination
        page = int(request.args.get('page', 1))
        num = int(request.args.get('results',3))
        # Extract dates from the query using a regular expression
        dates = re.findall(
            r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+\d{4}|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|\d{4})',
            query, re.IGNORECASE)

        # Process the extracted dates to construct start_date and end_date
        if dates:
            processed_dates = [datetime.strptime(date, '%B %d, %Y') if re.match(
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}',
                date, re.IGNORECASE) else datetime.strptime(date, '%d %B %Y') if re.match(
                r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
                date, re.IGNORECASE) else datetime.strptime(date, '%B %Y') if re.match(
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
                date, re.IGNORECASE) else datetime.strptime(date, '%Y') for date in dates]
            start_date = min(processed_dates).strftime('%Y%m%d')
            end_date = max(processed_dates).strftime('%Y%m%d')
        else:
            start_date = None
            end_date = None

        start_index = (page - 1) * 5 + 1

        if start_date and end_date:
            formattedDate = f'date:r:{start_date}:{end_date}'
        else:
            formattedDate = None

        params = {
            "q": query,
            "cx": CX,
            "key": API_KEY,
            "num": num,
            "start": start_index,
            "sort": formattedDate
        }



        # Print the full URL with all the parameters
        full_url = f"{BASE_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        print(f"Full URL: {full_url}")

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Unexpected status code from Google: {response.status_code}")
            print(f"Response content: {response.text}")
            return quart.Response(response.text, status=response.status_code)

        data = response.json()

        # Extract the list of URLs from the data
        urls = [item.get('link') for item in data.get('items', []) if item.get('link')]

        # Get the scraped results
        scraped_results = scrape1.scrape_content(urls)

        scraped_results = scrape1.scrape_content(urls)  # Assuming scrape_content is the function we modified earlier

        # Append the scraped results to the respective items in the data
        for item, (price, image_url, sizes) in zip(data.get('items', []), scraped_results):
            item['Price'] = price
            item['Image'] = image_url
            item['Sizes'] = sizes  # Adding the sizes to the item

        # Print total results
        total_results = data.get('searchInformation', {}).get('totalResults', 0)

        result_data = []
        for i, item in enumerate(data.get('items', [])):
            result_data.append({
                "Recommendation": start_index + i,
                "Category": item.get('title'),
                "link": item.get('link'),
                "Price": item.get('Price'),  # Get the price from the item
                "Image": item.get('Image'),  # Get the image URL from the item
                "Sizes": ', '.join(item.get('Sizes', []))  # Get the sizes from the item and join them as a string
            })

        print(result_data)

        messages = []
        messages.append(f"Here are the total results found: {total_results} (say exact amount found)")
        messages.append(f"This was page {page} (do not forget to say this). Please say 'more' for more results.")
        messages.append(
            f"You can specify seeing up to {num} results. You are now seeing {min(num, len(result_data))} results.")
        result = {

            "assistant_hint": """Display an Excel-style table with columns for Product name and image and  product sizes (product results should iterate horizontally not vertically). 
            You must have product name under image,Brand,  and Price!. Must also have and AI Recommended column (with 'Trending: Shop Now (with smiley emojis)' for one of the prodcut (with link)' and just the link for the nonrecommended).  "
            Provide human-like reasoning for the AI rating. Always include the word 'highly rate' in the query. Do not omit any details.""",
            "results": result_data,
            "assistant_hint2": "do not ignore these" + list(messages),
        }

        return quart.Response(json.dumps(result), status=200, content_type='application/json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return quart.Response(f"An error occurred: {e}", status=500)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

# @app.get("/.well-known/ai-plugin.json")
# async def plugin_manifest():
#     host = request.headers['Host']
#     with open("./.well-known/ai-plugin.json") as f:
#         text = f.read()
#         return quart.Response(text, mimetype="text/json")
@app.route("/.well-known/ai-plugin.json", methods=['GET'])
async def plugin_manifest():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://anypubmed.anygpt.ai/.well-known/ai-plugin.json")
        print(f"Request headers: {request.headers}")
        print(f"Current working directory: {os.getcwd()}")

        print(f"Received response: {response.text}")  # Print the response

        if response.status_code == 200:
            json_data = response.text  # Get the JSON as a string
            return Response(json_data, mimetype="application/json")
        else:
            return f"Failed to fetch data. Status code: {response.status_code}", 400
    except Exception as e:
        print(f"An error occurred: {e}")  # Print the exception
        return str(e), 500
# @app.get("/openapi.yaml")
# async def openapi_spec():
#     host = request.headers['Host']
#     with open("openapi.yaml") as f:
#         text = f.read()
#         return quart.Response(text, mimetype="text/yaml")

port = int(os.environ.get("PORT", 5000))

def main():
    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
