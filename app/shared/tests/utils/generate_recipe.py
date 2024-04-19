from decimal import Decimal
from random import randint
from typing import Optional

from core.models import Recipe
from django.conf import settings
from shared.utils.get_or_create_ingredients_for_recipe import get_or_create_ingredients_for_recipe
from shared.utils.get_or_create_tags_for_recipe import get_or_create_tags_for_recipe


def generate_sample_recipe_payload(user: Optional[settings.AUTH_USER_MODEL] = None, with_nested_fields=False, **params):
    defaults = {
        "time_to_make_in_minutes": randint(1, 180),
        "price": Decimal("5.25"),
        "description": "Sample description",
        "link": "http://example.com/recipe.pdf",
    }

    if user:
        defaults["user"] = user

    if "title" not in params:
        recipe_quantity = Recipe.objects.count()
        defaults["title"] = f"Sample Recipe {recipe_quantity}"

    if with_nested_fields:
        defaults["tags"] = [
            {
                "name": "Sample Tag 1",
            },
            {
                "name": "Sample Tag 2",
            },
        ]

        defaults["ingredients"] = [
            {
                "name": "Sample Ingredient 1",
            },
            {
                "name": "Sample Ingredient 2",
            },
        ]

    defaults.update(params)

    return defaults


def generate_sample_recipe(user: settings.AUTH_USER_MODEL, **params):
    payload = generate_sample_recipe_payload(user, **params)

    tags = payload.pop("tags", [])
    ingredients = payload.pop("ingredients", [])

    recipe = Recipe.objects.create(**payload)

    get_or_create_tags_for_recipe(recipe, tags)
    get_or_create_ingredients_for_recipe(recipe, ingredients)

    return recipe
