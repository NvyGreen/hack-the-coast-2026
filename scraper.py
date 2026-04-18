import json
from pathlib import Path

def load_tiktok_keywords():
    keywords_path = Path(__file__).resolve().parent / "datasets" / "tiktok_keywords.json"
    with keywords_path.open("r", encoding="utf-8") as f:
        keywords = json.load(f)
    return keywords

def scrape_tiktok_creative_center():
    # For now, just load the provided data
    keywords = load_tiktok_keywords()
    print(f"Loaded {len(keywords)} TikTok keywords with metrics.")
    # Save to creative_insights.json for consistency
    insights = {"keywords": keywords}
    with open('datasets/creative_insights.json', 'w') as f:
        json.dump(insights, f, indent=4)
    print("Data saved to datasets/creative_insights.json")
    return insights

if __name__ == "__main__":
    scrape_tiktok_creative_center()