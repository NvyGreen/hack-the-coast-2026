import sys
import os

# Ensure CWD is the project root so dataset paths in product.py resolve correctly
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(_project_root)
sys.path.insert(0, os.path.join(_project_root, "backend"))
sys.path.insert(0, _project_root)

from typing import Optional
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from backend.product import tiktok_registry, trend_registry
from backend.filtering import FilterIngredients

app = Flask(__name__)
CORS(app)

_filter = FilterIngredients()

# Derived directly from the 12 keys in datasets/categories.txt
CATEGORY_ICONS = {
    "American Ginseng":          "🌿",
    "Asian Ginseng":             "🌾",
    "Candies":                   "🍬",
    "Chocolates":                "🍫",
    "Cookies":                   "🍪",
    "Ginger":                    "🫚",
    "Instant Food/Seasonings":   "🍜",
    "Mooncakes":                 "🥮",
    "Nuts/Dried Fruits":         "🥜",
    "Supplements/Personal Care": "💊",
    "Teas/Instant Beverage":     "🍵",
    "Tiger Balm":                "🏮",
    "Other":                     "📦",
}

def _icon_for(category: str) -> str:
    # Exact match first
    if category in CATEGORY_ICONS:
        return CATEGORY_ICONS[category]
    # Partial match against the canonical category names
    cat_lower = (category or "").lower()
    for canonical, icon in CATEGORY_ICONS.items():
        if any(word in cat_lower for word in canonical.lower().split("/")):
            return icon
    return "📦"


def _is_approved(product) -> bool:
    try:
        return _filter.filter(product.allergens, product.country_of_origin)
    except Exception:
        return True


def _product_dict(p, rank: int) -> dict:
    score = p.signal_score
    # existing=1 means the keyword maps to PoP's existing category portfolio
    # existing=0 means it fell through to new_dataset → net-new / distribute opportunity
    existing = 1 if p.existing else 0
    badge = "Distribute" if existing else "Develop"
    approved = _is_approved(p)

    ingredients = p.ingredients or []
    if isinstance(ingredients, str):
        ingredients = [i.strip() for i in ingredients.split(",")]

    return {
        "rank":              rank,
        "name":              p.description,
        "category":          p.category,
        "signal":            round(score * 10, 1),
        "bar":               round(score * 100),
        "color":             ["#1B3A5C", "#2557A7", "#3A7BD5", "#4A8FE8", "#5FA3F5"][(rank - 1) % 5],
        "badge":             "hot" if score >= 0.7 else "new",
        "approved":          approved,
        "existing":          existing,
        "opportunity_type":  badge,
        "icon":              _icon_for(p.category),
        "shelf_life":        p.shelf_life_months,
        "country_of_origin": p.country_of_origin,
        "ingredients":       ingredients,
    }


def _ranked_candidates(limit: Optional[int] = None) -> list:
    candidates = []

    for p in tiktok_registry.all():
        if p.is_food_related:
            candidates.append(p)

    for products in trend_registry.all().values():
        for p in products:
            if p.is_food_related:
                candidates.append(p)

    candidates.sort(key=lambda p: p.signal_score, reverse=True)

    seen, deduped = set(), []
    for p in candidates:
        key = p.description.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(p)
            if limit and len(deduped) >= limit:
                break

    return deduped


def _build_top_products(limit: int = 5) -> list:
    return [_product_dict(p, i + 1) for i, p in enumerate(_ranked_candidates(limit))]


def _build_keywords() -> list:
    tiktok_products = sorted(
        [p for p in tiktok_registry.all() if p.is_food_related],
        key=lambda p: p.signal_score,
        reverse=True,
    )
    seen, keywords = set(), []
    for p in tiktok_products:
        kw = p.description.lower()
        if kw in seen:
            continue
        seen.add(kw)
        score = p.signal_score
        tier = "hot" if score >= 0.6 else "mid" if score >= 0.35 else "low"
        size = "xl" if score >= 0.8 else "lg" if score >= 0.6 else "md" if score >= 0.4 else "sm"
        keywords.append({"text": p.description, "tier": tier, "size": size})

    return keywords[:20]


def _build_opportunities(top_products: list) -> list:
    opps = []
    for p in top_products[:5]:
        badge = p["opportunity_type"]  # "Distribute" or "Develop"
        if badge == "Distribute":
            bc, bt = "#EBF3FD", "#185FA5"
        else:
            bc, bt = "#EAF5EE", "#2E7D52"
        opps.append({
            "icon":  p["icon"],
            "name":  p["name"],
            "sub":   f"{p['category']} — signal {p['signal']}/10",
            "badge": badge,
            "bc":    bc,
            "bt":    bt,
        })
    return opps


def _build_stats(top_products: list) -> dict:
    all_tiktok = tiktok_registry.all()
    all_trends = [p for products in trend_registry.all().values() for p in products]
    total      = len(all_tiktok) + len(all_trends)
    actionable = len([p for p in top_products if p["signal"] >= 6])
    fda_removed = len([p for p in top_products if not p["approved"]])
    return {
        "trends_scanned":     total,
        "actionable_signals": actionable,
        "pop_adjacencies":    len(top_products),
        "fda_flags_removed":  fda_removed,
    }


@app.route("/api/dashboard")
def dashboard():
    top_products = _build_top_products(limit=5)
    return jsonify({
        "top_products":  top_products,
        "keywords":      _build_keywords(),
        "opportunities": _build_opportunities(top_products),
        "stats":         _build_stats(top_products),
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


_frontend = os.path.join(_project_root, "frontend")

@app.route("/")
@app.route("/<path:filename>")
def serve_frontend(filename="index.html"):
    return send_from_directory(_frontend, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
