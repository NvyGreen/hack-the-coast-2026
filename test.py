from product import tiktok_registry

print("=== TIKTOK PRODUCTS ===")
for p in tiktok_registry.all():
    if not p.is_food_related:
        print(f"  [SKIP] {p.description!r:20s} | category_sim={p.category_sim:.3f}")
        continue
    print(f"  {p.description!r:20s} | category={p.category!r:28s} | cat_sim={p.category_sim:.3f} | sim={p.sim_score:.3f} | existing={p.is_existing} | signal={p.signal_score:.3f}")
