import json
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent / "datasets"

model = SentenceTransformer("all-MiniLM-L6-v2")

with (BASE / "product_sales_summary.json").open("r", encoding="utf-8") as f:
    product_sales_summary = json.load(f)


def _save_embeddings(path: Path, embeddings: dict) -> None:
    entries = {k: v.tolist() for k, v in embeddings.items()}
    lines = [f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in entries.items()]
    path.write_text("{\n" + ",\n".join(lines) + "\n}\n", encoding="utf-8")


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
        _save_embeddings(embeddings_path, category_embeddings)
    return category_embeddings

def get_newdataset_categories():
  
    embeddings_path = BASE / "new_dataset_embeddings.json"
    if embeddings_path.exists():
        with embeddings_path.open("r", encoding="utf-8") as f:
            new_embeddings = {k: np.array(v) for k, v in json.load(f).items()}
    else:
        with (BASE / "new_dataset.json").open("r", encoding="utf-8") as f:
            new_embeddings = json.load(f)
        new_embeddings = {
            category: model.encode(category)
            for category in new_embeddings.keys()
        }
        _save_embeddings(embeddings_path, new_embeddings)
    return new_embeddings


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
        _save_embeddings(embeddings_path, product_descr_embeddings)

    return product_descr_embeddings


def classify_product_by_category(product_name) -> Tuple[str, float]:
    """Returns (category, similarity_score)."""
    category_embeddings = get_categories()
    product_embedding = model.encode(product_name.lower())
    max_similarity = -1.0
    best_category = None
    for category, embedding in category_embeddings.items():
        sim = float(cosine_similarity([product_embedding], [embedding])[0][0])
        if sim > max_similarity:
            max_similarity = sim
            best_category = category
    return best_category, max_similarity


def exact_match_product(product_name):
    name_lower = product_name.lower()
    for product_id, product in product_sales_summary.items():
        if name_lower in product["description"].lower():
            return product_id
    return None

def classify_product_by_keyword(keyword: str) -> tuple[str, float]:
    """Match a short keyword (e.g. TikTok) against category keyword lists first,
    then fall back to embedding similarity. Returns (category, score)."""
    with (BASE / "categories.txt").open("r", encoding="utf-8") as f:
        categories_map = json.load(f)
    keyword_lower = keyword.lower()
    for category, keywords in categories_map.items():
        if keyword_lower in keywords:
            return category, 1.0
    category, score = classify_product_by_category(keyword)
    return category, score

def classify_product_newdataset(product_name) -> Tuple[Optional[str], float]:
    new_embeddings = get_newdataset_categories()
    name_lower = product_name.lower()
    product_embedding = model.encode(name_lower)
    best_match, max_similarity = None, -1.0
    for name, emb in new_embeddings.items():
        if name_lower in name.lower():
            return name, 1.0
        sim = float(cosine_similarity([product_embedding], [emb])[0][0])
        if sim > max_similarity:
            max_similarity = sim
            best_match = name
    return best_match, max_similarity

def get_newdataset_entry(product_name) -> Tuple[Optional[str], Optional[dict], float]:
    """Returns (name, full_data_dict, similarity) for the closest new_dataset.json entry."""
    with (BASE / "new_dataset.json").open("r", encoding="utf-8") as f:
        new_dataset = json.load(f)
    new_embeddings = get_newdataset_categories()
    name_lower = product_name.lower()
    product_embedding = model.encode(name_lower)
    best_match, max_similarity = None, -1.0
    for name, emb in new_embeddings.items():
        if name_lower in name.lower():
            return name, new_dataset.get(name), 1.0
        sim = float(cosine_similarity([product_embedding], [emb])[0][0])
        if sim > max_similarity:
            max_similarity = sim
            best_match = name
    return best_match, new_dataset.get(best_match) if best_match else None, max_similarity


def classify_product_by_description(product_name) -> Tuple[Optional[str], float]:
    """Returns (product_id, similarity_score). Score is 1.0 for exact string matches."""
    match = exact_match_product(product_name)
    if match:
        return match, 1.0
    product_descr_embeddings = get_product_descriptions()
    product_embedding = model.encode(product_name.lower())
    max_similarity = -1.0
    best_product_id = None
    for product_id, descr_embedding in product_descr_embeddings.items():
        sim = float(cosine_similarity([product_embedding], [descr_embedding])[0][0])
        if sim > max_similarity:
            max_similarity = sim
            best_product_id = product_id
    return best_product_id, max_similarity


if __name__ == "__main__":
    # Example usage
    #category_embeddings = get_categories()
    #print("Category Embeddings:", category_embeddings)

    #product_descr_embeddings = get_product_descriptions()
    #print("Product Description Embeddings:", product_descr_embeddings)

    new_embeddings = get_newdataset_categories()
    print("New Dataset Embeddings:", new_embeddings)

