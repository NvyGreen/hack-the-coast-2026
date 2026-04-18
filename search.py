import requests
import os
import time
from dotenv import load_dotenv

# Load variables from .env
load_dotenv() 
# Retrieve the key
API_KEY = os.getenv("CUSTOM_SEARCH_API")

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Rate limiting: wait 1 second between requests
    time.sleep(1)

    link = data["items"][0]["link"]
    return link


if __name__ == "__main__":
    from pytrends.request import TrendReq

    pytrends = TrendReq(hl='en-US', tz=360)

    food_items = ["pizza", "sushi", "tacos", "ramen"]

    pytrends.build_payload(food_items, timeframe='now 1-d', geo='US')

    # Interest over time
    try:
        df = pytrends.interest_over_time()
        print("df shape:", df.shape)
        print(df)
    except Exception as e:
        print("Error:", e)

    # Related queries per keyword
    related = pytrends.related_queries()
    for item in food_items:
        print(f"\n{item} - top:", related[item]['top'])