import json

def trends_per_category():
    with open("datasets/trends_data.json", "r") as f:
        trends_data = json.load(f)
        item_trends = {}
        for category, trends in trends_data.items():
            item_trends[category] = []
            for item in trends["related_queries"]["top"][:5]:
                item_trends[category].append((item["query"], item["value"]))
    
    return item_trends


if __name__ == "__main__":
    item_trends = trends_per_category()
    for category, trends in item_trends.items():
        print(f"Category: {category}")
        for query, value in trends:
            print(f"  {query}: {value}")


