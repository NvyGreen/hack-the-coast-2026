import json
import time
from pathlib import Path
from pytrends.request import TrendReq

CATEGORIES_PATH = Path(__file__).resolve().parent.parent / "datasets" / "categories.txt"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "datasets" / "trends_data.json"


def fetch_category(pytrends, category):
    keyword = category.lower()
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

    iot_df = pytrends.interest_over_time()
    if keyword in iot_df.columns:
        iot_df = iot_df[[keyword]]
    else:
        cols = [c for c in iot_df.columns if c != 'isPartial']
        iot_df = iot_df[cols] if cols else iot_df.drop(columns=['isPartial'], errors='ignore')

    rq = pytrends.related_queries()
    if keyword in rq and rq[keyword]['top'] is not None:
        related = {
            'top': rq[keyword]['top'].to_dict('records'),
            'rising': rq[keyword]['rising'].to_dict('records') if rq[keyword]['rising'] is not None else []
        }
    else:
        related = {'top': [], 'rising': []}

    return {
        'interest_over_time': json.loads(iot_df.to_json()),
        'related_queries': related
    }


def needs_fetch(entry):
    """Return True if the category still needs fetching."""
    if not entry:
        return True
    if 'error' in entry:
        return True
    iot = entry.get('interest_over_time', {})
    rq = entry.get('related_queries', {})
    # Matches the exact empty structure: {} interest_over_time + empty top/rising
    if iot == {} and rq.get('top') == [] and rq.get('rising') == []:
        return True
    return False


def run_fetcher():
    with CATEGORIES_PATH.open("r", encoding="utf-8") as f:
        categories = json.load(f)

    if OUTPUT_PATH.exists():
        with OUTPUT_PATH.open("r", encoding="utf-8") as f:
            trends_data = json.load(f)
    else:
        trends_data = {}

    pytrends = TrendReq(hl='en-US', tz=360)

    pending = [cat for cat in categories if needs_fetch(trends_data.get(cat))]
    print(f"{len(pending)} categories to fetch: {pending}")

    for category in pending:
        print(f"Fetching: {category}")
        try:
            trends_data[category] = fetch_category(pytrends, category)
            print(f"  OK: {category}")
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"  Rate limited. Waiting 60s and skipping...")
                time.sleep(60)
            else:
                print(f"  Error: {e}")
            trends_data[category] = {"error": error_msg}

        with OUTPUT_PATH.open("w", encoding="utf-8") as f:
            json.dump(trends_data, f, indent=4)

        time.sleep(60)

    print("Done. Trends data saved to datasets/trends_data.json")


if __name__ == "__main__":
    run_fetcher()
