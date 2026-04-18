from product import tiktok_registry, trend_registry

print("=== TIKTOK PRODUCTS ===")
for p in tiktok_registry.all():
    if not p.is_food_related:
        print(f"  [SKIP] {p.description!r:30s} | category_sim={p.category_sim:.3f}")
        continue
    print(
        f"  {p.description!r:30s} | category={p.category!r:28s}"
        f" | shelf_life={str(p.shelf_life_months)!r:10s}"
        f" | country={str(p.country_of_origin)!r:20s}"
        f" | cat_sim={p.category_sim:.3f} | signal={round(p.signal_score * 10 * 2) / 2}/10"
    )

print()
print("=== GOOGLE SEARCH CATEGORIES ===")
for category, products in trend_registry.all().items():
    for p in products:
        if not p.is_food_related:
            print(f"  [SKIP] {p.description!r:30s} | category_sim={p.category_sim:.3f}")
            continue
        print(
            f"  {p.description!r:30s} | category={p.category!r:28s}"
            f" | shelf_life={str(p.shelf_life_months)!r:10s}"
            f" | country={str(p.country_of_origin)!r:20s}"
            f" | cat_sim={p.category_sim:.3f} | signal={round(p.signal_score * 10 * 2) / 2}/10"
        )
