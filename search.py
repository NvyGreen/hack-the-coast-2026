import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv() 

# Retrieve the key
API_KEY = os.getenv("CUSTOM_SEARCH_API")


def search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    link = data["items"][0]["link"]
    return link