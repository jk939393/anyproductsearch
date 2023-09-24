import quart
import quart_cors
from quart import request
import requests
import os
import re
from datetime import datetime
import urllib.parse
import json
import httpx
API_KEY = "AIzaSyBbvhM0tfQDlrI2ndRbZAN1YKBmwwStIrw"
CX = "c660620618b3f4e27"
BASE_URL = "https://www.googleapis.com/customsearch/v1/siterestrict"

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.route("/")
async def hello():
    return "Hello, World 01 "


@app.route("/google_search/<string:query>", methods=['GET'])
async def get_google_search_results(query, page=1):
    try:
        query = f"{query} highly rated for adults"
        page = int(request.args.get('page', 1))
        num = int(request.args.get('results', 3))

        start_index = (page - 1) * 5 + 1

        params = {
            "q": query,
            "cx": CX,
            "key": API_KEY,
            "num": num,
            "start": start_index
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            return quart.Response(response.text, status=response.status_code)

        data = response.json()

        result_data = []
        for i, item in enumerate(data.get('items', [])):
            # Extract image link
            image_link = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src', None)

            result_data.append({
                "Recommendation": start_index + i,
                "Category": item.get('title'),
                "link": item.get('link'),
                "Image": image_link
            })

        total_results = data.get('searchInformation', {}).get('totalResults', 0)

        messages = []
        messages.append(f"Here are the total results found: {total_results}")
        messages.append(f"This was page {page}. Please say 'more' for more results.")
        messages.append(
            f"You can specify seeing up to {num} results. You are now seeing {min(num, len(result_data))} results.")

        result = {
            "assistant_hint": """Provide human-like reasoning for the AI rating. Always include the word 'highly rate' in the query. Do not omit any details.""",
            "results": result_data,
            "assistant_hint2": messages,
        }

        return quart.Response(json.dumps(result), status=200, content_type='application/json')
    except Exception as e:
        return quart.Response(f"An error occurred: {e}", status=500)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.route("/.well-known/ai-plugin.json", methods=['GET'])
async def plugin_manifest():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://anypubmed.anygpt.ai/.well-known/ai-plugin.json")

        if response.status_code == 200:
            json_data = response.text
            return Response(json_data, mimetype="application/json")
        else:
            return f"Failed to fetch data. Status code: {response.status_code}", 400
    except Exception as e:
        return str(e), 500


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


port = int(os.environ.get("PORT", 5000))


def main():
    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
