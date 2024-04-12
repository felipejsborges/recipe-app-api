from random import randint

from core.models import Recipe
from django.urls import reverse
from recipes.serializers import RecipesSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_recipe import generate_sample_recipe, generate_sample_recipe_payload
from shared.tests.utils.generate_user import generate_sample_user

RECIPES_INDEX_URL = reverse("recipes:recipe-list")


class RecipesIndexNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(RECIPES_INDEX_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_post_unauthenticated(self):
        res = self.client.post(RECIPES_INDEX_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class RecipesIndexNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
#     def test_put_detail_not_allowed(self):
#         res = self.client.put(RECIPES_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_patch_detail_not_allowed(self):
#         res = self.client.patch(RECIPES_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_delete_detail_not_allowed(self):
#         res = self.client.delete(RECIPES_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateRecipeApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_create_recipe_happy_path(self):
        payload = generate_sample_recipe_payload(user=self.user)

        res = self.client.post(RECIPES_INDEX_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        self.assertEqual(recipe.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)


class ListRecipesApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_list_recipes_happy_path(self):
        random_quantity = randint(2, 5)
        for _ in range(random_quantity):
            generate_sample_recipe(user=self.user)

        res = self.client.get(RECIPES_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        existing_recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipesSerializer(existing_recipes, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        random_quantity_linked_to_other_user = randint(1, 3)
        for _ in range(random_quantity_linked_to_other_user):
            other_user = generate_sample_user()
            generate_sample_recipe(user=other_user)

        random_quantity = randint(1, 3)
        for _ in range(random_quantity):
            generate_sample_recipe(user=self.user)

        res = self.client.get(RECIPES_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipesSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)
