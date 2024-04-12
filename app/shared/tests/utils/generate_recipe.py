from decimal import Decimal
from random import randint

from core.models import Recipe
from django.conf import settings


def generate_sample_recipe_payload(user: settings.AUTH_USER_MODEL, **params):
    defaults = {
        "time_to_make_in_minutes": randint(1, 180),
        "price": Decimal("5.25"),
        "description": "Sample description",
        "link": "http://example.com/recipe.pdf",
        "user": user,
    }

    if "title" not in params:
        recipe_quantity = Recipe.objects.count()
        defaults["title"] = f"Sample Recipe {recipe_quantity}"

    defaults.update(params)

    return defaults


def generate_sample_recipe(user: settings.AUTH_USER_MODEL, **params):
    payload = generate_sample_recipe_payload(user, **params)

    return Recipe.objects.create(**payload)
