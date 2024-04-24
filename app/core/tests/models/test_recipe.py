from decimal import Decimal
from unittest.mock import patch

from core import models
from core.models.recipe import get_recipe_image_path
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


class GetRecipeImagePathTests(TestCase):
    @patch("core.models.recipe.uuid.uuid4")
    def test_get_recipe_image_path_happy_path(self, mock_uuid):
        uuid = "sample-uuid"

        mock_uuid.return_value = uuid

        file_path = get_recipe_image_path(None, "anything.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
