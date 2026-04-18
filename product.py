import json
from pathlib import Path
from typing import Optional

_DATA_PATH   = Path(__file__).resolve().parent / "datasets" / "product_sales_summary.json"
_TRENDS_PATH = Path(__file__).resolve().parent / "datasets" / "trends_data.json"
_TIKTOK_PATH = Path(__file__).resolve().parent / "datasets" / "tiktok_keywords.json"

with _DATA_PATH.open("r", encoding="utf-8") as f:
    _product_data = json.load(f)

# Cosine similarity below this means the trend has no close catalog match
_NOVEL_THRESHOLD = 0.50

with _TRENDS_PATH.open("r", encoding="utf-8") as f:
    _trends_data = json.load(f)


# ── Existing product ──────────────────────────────────────────────────────────

class Product:
    def __init__(self, product_id: str):
        if product_id not in _product_data:
            raise KeyError(f"Product ID '{product_id}' not found in product_sales_summary.json")
        self.id = product_id
        data = _product_data[product_id]
        self.description       = data["description"]
        self.order_count       = data["order_count"]
        self.total_qty_shipped = data["total_qty_shipped"]
        self.total_revenue     = data["total_revenue"]
        self.avg_unit_cost     = data["avg_unit_cost"]
        self.min_unit_cost     = data["min_unit_cost"]
        self.max_unit_cost     = data["max_unit_cost"]
        self.country_of_origin = data["country_of_origin"]
        self.shelf_life_months = data["shelf_life_months"]
        self.allergens         = data["allergens"]

    def __repr__(self):
        return f"Product({self.id!r}, {self.description!r})"


# ── Shared base for new/external products ────────────────────────────────────

class _NewProductBase:
    """Shared lazy properties for products sourced outside the catalog."""
    description: str

    def __init__(self):
        self.order_count       = None
        self.total_qty_shipped = None
        self.total_revenue     = None
        self.avg_unit_cost     = None
        self._category         = None
        self._category_sim     = None
        self._closest_id       = None
        self._closest_sim      = None
        self._signal_score     = None

    def _resolve_closest(self):
        """Run embedding search once and cache both product_id and similarity score."""
        if self._closest_id is None:
            import categories
            self._closest_id, self._closest_sim = categories.classify_product_by_description(self.description)

    @property
    def category(self) -> str:
        if self._category is None:
            import categories
            self._category, self._category_sim = categories.classify_product_by_category(self.description)
        return self._category

    @property
    def category_sim(self) -> Optional[float]:
        _ = self.category  # ensure resolved
        return self._category_sim

    @property
    def is_food_related(self) -> bool:
        return self.category_sim is not None and self.category_sim >= 0.30

    @property
    def closest_product_id(self) -> Optional[str]:
        self._resolve_closest()
        return self._closest_id

    @property
    def sim_score(self) -> Optional[float]:
        self._resolve_closest()
        return self._closest_sim

    @property
    def is_existing(self) -> bool:
        """True if this trend is close enough to a catalog product to reuse its metadata."""
        return self._closest_sim is not None and self._closest_sim >= _NOVEL_THRESHOLD

    @property
    def signal_score(self) -> float:
        raise NotImplementedError


# ── Google Trends product ─────────────────────────────────────────────────────

class GoogleTrendProduct(_NewProductBase):
    """A trending search query from Google Trends related_queries."""

    def __init__(self, query: str, value: int, category_trends: dict):
        super().__init__()
        self.description      = query
        self.value            = value
        self._category_trends = category_trends

    @property
    def signal_score(self) -> float:
        if self._signal_score is None:
            import opportunities
            self._signal_score = opportunities.signal_strength(self, self._category_trends)
        return self._signal_score

    def __repr__(self):
        return f"GoogleTrendProduct({self.description!r}, value={self.value})"


# ── TikTok product ────────────────────────────────────────────────────────────

class TikTokProduct(_NewProductBase):
    """A trending keyword from TikTok ad/social data."""

    def __init__(self, data: dict):
        super().__init__()
        self.description      = data["keyword"]
        self.rank             = data.get("rank")
        self.popularity       = data.get("popularity")
        self.popularity_change = data.get("popularity_change")
        self.ctr              = data.get("ctr")
        self.cvr              = data.get("cvr")
        self.cpa              = data.get("cpa")
        self.cost             = data.get("cost")
        self.impressions      = data.get("impressions")
        self.view_rate_6s     = data.get("6s_view_rate")
        self.likes            = data.get("likes")
        self.shares           = data.get("shares")
        self.comments         = data.get("comments")
        self._raw             = data

    @property
    def category(self) -> str:
        if self._category is None:
            import categories
            self._category, self._category_sim = categories.classify_product_by_keyword(self.description)
        return self._category

    @property
    def signal_score(self) -> float:
        if self._signal_score is None:
            import opportunities
            self._signal_score = opportunities.socialmedia_signal_strength(self._raw)
        return self._signal_score

    def __repr__(self):
        return f"TikTokProduct({self.description!r}, rank={self.rank})"


# ── Registries ────────────────────────────────────────────────────────────────

class ProductRegistry:
    """Registry for existing catalog products."""

    def __init__(self):
        self._registry: dict[str, Product] = {}

    def get(self, product_id: str) -> Product:
        if product_id not in self._registry:
            self._registry[product_id] = Product(product_id)
        return self._registry[product_id]

    def load_all(self) -> None:
        for product_id in _product_data:
            self.get(product_id)

    def all(self) -> dict[str, Product]:
        self.load_all()
        return self._registry

    def __contains__(self, product_id: str) -> bool:
        return product_id in _product_data


class TrendRegistry:
    """Registry of GoogleTrendProducts built from trends_data.json related queries."""

    def __init__(self):
        self._by_category: dict[str, list[GoogleTrendProduct]] = {}
        self._built = False

    def _build(self):
        if self._built:
            return
        for category, trends in _trends_data.items():
            top = trends.get("related_queries", {}).get("top", [])[:5]
            self._by_category[category] = [
                GoogleTrendProduct(item["query"], item["value"], trends)
                for item in top
            ]
        self._built = True

    def get_by_category(self, category: str) -> list[GoogleTrendProduct]:
        self._build()
        return self._by_category.get(category, [])

    def all(self) -> dict[str, list[GoogleTrendProduct]]:
        self._build()
        return self._by_category


class TikTokRegistry:
    """Registry of TikTokProducts built from tiktok_keywords.json."""

    def __init__(self):
        self._registry: list[TikTokProduct] = []
        self._built = False

    def _build(self, limit: int = 30):
        if self._built:
            return
        with _TIKTOK_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self._registry = [TikTokProduct(item) for item in data[:limit]]
        self._built = True

    def all(self) -> list[TikTokProduct]:
        self._build()
        return self._registry


# ── Module-level singletons ───────────────────────────────────────────────────

registry       = ProductRegistry()
trend_registry = TrendRegistry()
tiktok_registry = TikTokRegistry()
