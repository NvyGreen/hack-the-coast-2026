import json
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent / "datasets"

model = SentenceTransformer("all-MiniLM-L6-v2")

with (BASE / "product_sales_summary.json").open("r", encoding="utf-8") as f:
    product_sales_summary = json.load(f)


def get_categories():
  
    embeddings_path = BASE / "category_embeddings.json"
    if embeddings_path.exists():
        with embeddings_path.open("r", encoding="utf-8") as f:
            category_embeddings = {k: np.array(v) for k, v in json.load(f).items()}
    else:
        with (BASE / "categories.txt").open("r", encoding="utf-8") as f:
            categories = json.load(f)
        category_embeddings = {
            category: model.encode(category)
            for category in categories.keys()
        }
        with embeddings_path.open("w", encoding="utf-8") as f:
            json.dump({k: v.tolist() for k, v in category_embeddings.items()}, f)
    return category_embeddings


def get_product_descriptions():
    embeddings_path = BASE / "product_descr_embeddings.json"
    if embeddings_path.exists():
        with embeddings_path.open("r", encoding="utf-8") as f:
            product_descr_embeddings = {k: np.array(v) for k, v in json.load(f).items()}
    else:
        product_descr_embeddings = {
            product_id: model.encode(product["description"])
            for product_id, product in product_sales_summary.items()
        }
        with embeddings_path.open("w", encoding="utf-8") as f:
            json.dump({k: v.tolist() for k, v in product_descr_embeddings.items()}, f)

    return product_descr_embeddings


def classify_product_by_category(product_name):
    category_embeddings = get_categories()
    product_name = product_name.lower()
    product_embedding = model.encode(product_name)
    max_similarity = -1
    best_category = None
    for category, embedding in category_embeddings.items():
        sim = cosine_similarity([product_embedding], [embedding])[0][0]
        if sim > max_similarity:
            max_similarity = sim
            best_category = category
    return best_category


def build_description_index():
    index = {}
    for product_id, product in product_sales_summary.items():
        for word in product["description"].lower().split():
            index.setdefault(word, []).append(product_id)
    return index

_description_index = build_description_index()

def exact_match_product(product_name):
    words = product_name.lower().split()
    scores = {}
    for word in words:
        for product_id in _description_index.get(word, []):
            scores[product_id] = scores.get(product_id, 0) + 1
    if not scores:
        return None
    return max(scores, key=scores.get)


def classify_product_by_description(product_name):
    match = exact_match_product(product_name)
    if match:
        return match
    product_descr_embeddings = get_product_descriptions()
    product_name = product_name.lower()
    product_embedding = model.encode(product_name)
    max_similarity = -1
    best_product_id = None
    for product_id, descr_embedding in product_descr_embeddings.items():
        sim = cosine_similarity([product_embedding], [descr_embedding])[0][0]
        if sim > max_similarity:
            max_similarity = sim
            best_product_id = product_id
    return best_product_id
