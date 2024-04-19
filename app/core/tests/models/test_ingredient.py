from core import models
from django.test import TestCase
from shared.tests.utils.generate_user import generate_sample_user


class IngredientModelTests(TestCase):
    def test_create_ingredient(self):
        user = generate_sample_user()

        ingredient = models.Ingredient.objects.create(
            user=user,
            name="Sample ingredient",
        )

        self.assertEqual(str(ingredient), ingredient.name)
