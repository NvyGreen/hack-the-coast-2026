import csv
import json
from pathlib import Path
from collections import defaultdict

PO_CSV = Path(__file__).resolve().parent / "datasets" / "POP_PurchaseOrderHistory.XLSX - PO Order History 2023-2025.csv"
SPEC_CSV = Path(__file__).resolve().parent / "datasets" / "POP_ItemSpecMaster.xlsx - Item Spec Master.csv"
OUTPUT_PATH = Path(__file__).resolve().parent / "datasets" / "product_sales_summary.json"


def parse_float(val):
    try:
        return float(val.replace(",", "").strip()) if val.strip() else 0.0
    except ValueError:
        return 0.0


def parse_int(val):
    try:
        return int(float(val.replace(",", "").strip())) if val.strip() else 0
    except ValueError:
        return 0


# Load item spec master: Country of Origin, Shelf Life, Allergens
spec = {}
with SPEC_CSV.open("r", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        item = row["Item Number"].strip()
        if item:
            spec[item] = {
                "country_of_origin": row.get("Country of Origin", "").strip() or None,
                "shelf_life_months": row.get("Shelf Life (Months)", "").strip() or None,
                "allergens": row.get("Allergens", "").strip() or None,
            }

# Aggregate purchase order history per item
products = defaultdict(lambda: {
    "description": "",
    "total_qty_shipped": 0,
    "total_revenue": 0.0,
    "order_count": 0,
    "unit_costs": [],
})

with PO_CSV.open("r", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        item = row["Item Number"].strip()
        if not item:
            continue
        p = products[item]
        p["description"] = row["Item Description"].strip()
        p["total_qty_shipped"] += parse_int(row["QTY Shipped"])
        p["total_revenue"] += parse_float(row["Extended Cost"])
        p["order_count"] += 1
        unit_cost = parse_float(row["Unit Cost"])
        if unit_cost > 0:
            p["unit_costs"].append(unit_cost)

# Build output, sorted by revenue descending
summary = {}
for item, p in sorted(products.items(), key=lambda x: x[1]["total_revenue"], reverse=True):
    costs = p["unit_costs"]
    s = spec.get(item, {})
    summary[item] = {
        "description": p["description"],
        "order_count": p["order_count"],
        "total_qty_shipped": p["total_qty_shipped"],
        "total_revenue": round(p["total_revenue"], 2),
        "avg_unit_cost": round(sum(costs) / len(costs), 4) if costs else None,
        "min_unit_cost": round(min(costs), 4) if costs else None,
        "max_unit_cost": round(max(costs), 4) if costs else None,
        "country_of_origin": s.get("country_of_origin"),
        "shelf_life_months": s.get("shelf_life_months"),
        "allergens": s.get("allergens"),
    }

with OUTPUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

print(f"Saved {len(summary)} products to {OUTPUT_PATH}")
for item, p in list(summary.items())[:5]:
    print(f"  {item} | {p['description'][:38]} | ${p['total_revenue']:,.0f} | origin={p['country_of_origin']}")
