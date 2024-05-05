from random import randint

from core.models import Ingredient
from django.urls import reverse
from ingredients.serializers import IngredientsSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_ingredient import generate_sample_ingredient, generate_sample_ingredient_payload
from shared.tests.utils.generate_user import generate_sample_user

INGREDIENTS_INDEX_URL = reverse("ingredients:ingredient-list")


class IngredientsIndexNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(INGREDIENTS_INDEX_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_post_unauthenticated(self):
        res = self.client.post(INGREDIENTS_INDEX_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class IngredientsIndexNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
#     def test_put_detail_not_allowed(self):
#         res = self.client.put(INGREDIENTS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_patch_detail_not_allowed(self):
#         res = self.client.patch(INGREDIENTS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_delete_detail_not_allowed(self):
#         res = self.client.delete(INGREDIENTS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateIngredientApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_create_ingredient_happy_path(self):
        payload = generate_sample_ingredient_payload(user=self.user)

        res = self.client.post(INGREDIENTS_INDEX_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingredient = Ingredient.objects.get(id=res.data["id"])
        self.assertEqual(ingredient.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(ingredient, k), v)


class ListIngredientsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_list_ingredients_happy_path(self):
        random_quantity = randint(2, 5)
        for _ in range(random_quantity):
            generate_sample_ingredient(user=self.user)

        res = self.client.get(INGREDIENTS_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        existing_ingredients = Ingredient.objects.all().order_by("name")
        serializer = IngredientsSerializer(existing_ingredients, many=True)
        self.assertEqual(res.data["results"], serializer.data)

    def test_ingredient_list_limited_to_user(self):
        random_quantity_linked_to_other_user = randint(1, 3)
        for _ in range(random_quantity_linked_to_other_user):
            other_user = generate_sample_user()
            generate_sample_ingredient(user=other_user)

        random_quantity = randint(1, 3)
        for _ in range(random_quantity):
            generate_sample_ingredient(user=self.user)

        res = self.client.get(INGREDIENTS_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(user=self.user).order_by("name")
        serializer = IngredientsSerializer(ingredients, many=True)
        self.assertEqual(res.data["results"], serializer.data)
