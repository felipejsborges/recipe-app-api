from typing import Dict, List

from core.models import Ingredient, Recipe


def get_or_create_ingredients_for_recipe(recipe: Recipe, ingredients: List[Dict[str, str]]):
    for ingredient in ingredients:
        ingredient_obj, _ = Ingredient.objects.get_or_create(
            user=recipe.user,
            **ingredient,
        )

        recipe.ingredients.add(ingredient_obj)
