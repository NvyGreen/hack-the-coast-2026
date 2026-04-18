import json
import time
from pathlib import Path
from pytrends.request import TrendReq

# Load categories
categories_path = Path(__file__).resolve().parent / "datasets" / "categories.txt"
with categories_path.open("r", encoding="utf-8") as f:
    categories = json.load(f)

# Initialize pytrends with rate limiting
pytrends = TrendReq(hl='en-US', tz=360)

# Load existing trends data if available
output_path = Path(__file__).resolve().parent / "datasets" / "trends_data.json"
if output_path.exists():
    with output_path.open("r", encoding="utf-8") as f:
        trends_data = json.load(f)
else:
    trends_data = {}

for category, keywords in categories.items():
    # Skip if already successfully fetched
    if category in trends_data and "error" not in trends_data[category]:
        continue
    
    # Limit to 5 keywords per request
    kw_list = keywords[:5]
    if not kw_list:
        continue

    try:
        # Build payload
        pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')

        # Get interest over time
        interest_over_time_df = pytrends.interest_over_time()

        # Get related queries
        related_queries = pytrends.related_queries()
        related_data = {}
        for kw in kw_list:
            if kw in related_queries and related_queries[kw]['top'] is not None:
                related_data[kw] = {
                    'top': related_queries[kw]['top'].to_dict('records') if related_queries[kw]['top'] is not None else [],
                    'rising': related_queries[kw]['rising'].to_dict('records') if related_queries[kw]['rising'] is not None else []
                }
            else:
                related_data[kw] = {'top': [], 'rising': []}

        # Store both
        trends_data[category] = {
            'interest_over_time': interest_over_time_df.to_json(),
            'related_queries': related_data
        }

        # Rate limiting: wait 60 seconds between requests to avoid 429 errors
        time.sleep(60)

    except Exception as e:
        print(f"Error fetching trends for {category}: {e}")
        trends_data[category] = {"error": str(e)}

# Save to JSON
with output_path.open("w", encoding="utf-8") as f:
    json.dump(trends_data, f, indent=4)

print("Trends data saved to datasets/trends_data.json")