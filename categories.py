import json
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load categories from a dataset file
categories_path = Path(__file__).resolve().parent / "datasets" / "categories.txt"
with categories_path.open("r", encoding="utf-8") as f:
    categories = json.load(f)

# Load pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Pre-compute embeddings for all keywords
keyword_embeddings = {
    keyword: model.encode(keyword)
    for keywords in categories.values()
    for keyword in keywords
}

def classify_product(product_name):
    product_name = product_name.lower()
    product_embedding = model.encode(product_name)
    max_similarity = -1
    best_category = None
    for category, keywords in categories.items():
        for keyword in keywords:
            if product_name == keyword.lower():
                return category
            sim = cosine_similarity(
                [product_embedding],
                [keyword_embeddings[keyword]]
            )[0][0]
            if sim > max_similarity:
                max_similarity = sim
                best_category = category
    return best_category