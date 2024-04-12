from decimal import Decimal

from core import models
from django.test import TestCase
from shared.tests.utils.generate_user import generate_sample_user


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        user = generate_sample_user()

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_to_make_in_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)
