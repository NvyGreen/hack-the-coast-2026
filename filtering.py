# Shelf life in months
# Allergens: string or None
# Country as string
import categories
from product import registry

class FilterIngredients:
    def __init__(self):
        with open("datasets/restrictions/ingredients.txt", "r") as i:
            self.banned_ingredients = set(i.read().splitlines())

        with open("datasets/restrictions/countries.txt", "r") as c:
            self.restricted_countries = set(c.read().splitlines())

    def filter(self, allergens, country):
        if country in self.restricted_countries:
            return False

        if allergens:
            for allergen in allergens.split(","):
                if allergen.strip() in self.banned_ingredients:
                    return False

        return True

    def filter_by_product(self, product_name):
        prod_id = categories.exact_match_product(product_name)
        if not prod_id:
            prod_id = categories.classify_product_by_description(product_name)
        product = registry.get(prod_id)
        return self.filter(product.allergens, product.country_of_origin)