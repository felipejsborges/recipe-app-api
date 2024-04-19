from core.models import Ingredient
from django.urls import reverse
from ingredients.serializers import IngredientsSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_ingredient import generate_sample_ingredient
from shared.tests.utils.generate_user import generate_sample_user

INGREDIENTS_DETAIL_URL = "ingredients:ingredient-detail"


def generate_url_to_ingredient_detail(ingredient_id=None):
    return reverse(INGREDIENTS_DETAIL_URL, args=[ingredient_id])


class IngredientDetailNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(generate_url_to_ingredient_detail())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_put_unauthenticated(self):
        res = self.client.put(generate_url_to_ingredient_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_patch_unauthenticated(self):
        res = self.client.patch(generate_url_to_ingredient_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_delete_unauthenticated(self):
        res = self.client.delete(generate_url_to_ingredient_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class IngredientDetailNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_post_detail_not_allowed(self):
        res = self.client.post(generate_url_to_ingredient_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetIngredientApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_get_ingredient_happy_path(self):
        ingredient = generate_sample_ingredient(user=self.user)

        url = generate_url_to_ingredient_detail(ingredient.id)
        res = self.client.get(url)

        serializer = IngredientsSerializer(ingredient)
        self.assertEqual(res.data, serializer.data)


class UpdateIngredientApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_full_update(self):
        ingredient = generate_sample_ingredient(user=self.user)

        payload = {
            "name": "New ingredient name",
        }

        url = generate_url_to_ingredient_detail(ingredient.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredient.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(ingredient, k), v)
        self.assertEqual(ingredient.user, self.user)

    def test_update_ingredient_user_fails(self):
        ingredient = generate_sample_ingredient(user=self.user)

        other_user = generate_sample_user()
        payload = {"user": other_user.id}

        url = generate_url_to_ingredient_detail(ingredient.id)
        self.client.patch(url, payload)

        ingredient.refresh_from_db()

        self.assertEqual(ingredient.user, self.user)


class DeleteIngredientApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_delete_ingredient_happy_path(self):
        ingredient = generate_sample_ingredient(user=self.user)

        url = generate_url_to_ingredient_detail(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())

    def test_not_delete_ingredient_of_other_user(self):
        other_user = generate_sample_user()
        ingredient = generate_sample_ingredient(user=other_user)

        url = generate_url_to_ingredient_detail(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Ingredient.objects.filter(id=ingredient.id).exists())
