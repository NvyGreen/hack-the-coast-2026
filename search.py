import googlesearch

response = list(googlesearch.search("cool food items", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"))
print(f"Found {len(response)} results")
for result in response:
    print("Title: " + result.title)
    print("Description: " + result.description)
    print("URL: " + result.url)
    print("---")

