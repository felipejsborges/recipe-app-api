from core.models import Ingredient
from django.conf import settings


def generate_sample_ingredient_payload(user: settings.AUTH_USER_MODEL, **params):
    defaults = {
        "user": user,
    }

    if "name" not in params:
        ingredient_quantity = Ingredient.objects.count()
        defaults["name"] = f"Sample Ingredient {ingredient_quantity}"

    defaults.update(params)

    return defaults


def generate_sample_ingredient(user: settings.AUTH_USER_MODEL, **params):
    payload = generate_sample_ingredient_payload(user, **params)

    return Ingredient.objects.create(**payload)
