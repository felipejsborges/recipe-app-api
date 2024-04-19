from core.models import Recipe
from django.urls import reverse
from recipes.serializers import RecipeDetailSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_recipe import generate_sample_recipe
from shared.tests.utils.generate_user import generate_sample_user

RECIPES_DETAIL_URL = "recipes:recipe-detail"


def generate_url_to_recipe_detail(recipe_id=None):
    return reverse(RECIPES_DETAIL_URL, args=[recipe_id])


class RecipeDetailNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(generate_url_to_recipe_detail())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_put_unauthenticated(self):
        res = self.client.put(generate_url_to_recipe_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_patch_unauthenticated(self):
        res = self.client.patch(generate_url_to_recipe_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_delete_unauthenticated(self):
        res = self.client.delete(generate_url_to_recipe_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeDetailNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_post_detail_not_allowed(self):
        res = self.client.post(generate_url_to_recipe_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetRecipeApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_get_recipe_happy_path(self):
        recipe = generate_sample_recipe(user=self.user)

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)


class UpdateRecipeApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_partial_update_happy_path(self):
        original_link = "https://original.com/recipe.pdf"

        recipe = generate_sample_recipe(user=self.user, link=original_link)

        payload = {"title": "New recipe title"}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)

    def test_full_update(self):
        recipe = generate_sample_recipe(user=self.user)

        payload = {
            "title": "New recipe title",
            "link": "https://example.com/new-recipe.pdf",
            "description": "New recipe description",
            "time_to_make_in_minutes": recipe.time_to_make_in_minutes + 1,
            "price": recipe.price + 1,
        }

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_recipe_user_fails(self):
        recipe = generate_sample_recipe(user=self.user)

        other_user = generate_sample_user()
        payload = {"user": other_user.id}

        url = generate_url_to_recipe_detail(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)


class UpdateRecipeWithTagsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_update_recipe_adding_tags(self):
        recipe = generate_sample_recipe(user=self.user)

        payload = {"tags": [{"name": "New Tag"}]}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.tags.count(), len(payload["tags"]))

        for tag in payload["tags"]:
            exists_tag_with_same_name_of_payload = recipe.tags.filter(
                name=tag["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_tag_with_same_name_of_payload)

    def test_update_recipe_changing_tags(self):
        recipe = generate_sample_recipe(user=self.user, with_nested_fields=True)

        payload = {"tags": [{"name": "New Tag"}]}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.tags.count(), len(payload["tags"]))

        for tag in payload["tags"]:
            exists_tag_with_same_name_of_payload = recipe.tags.filter(
                name=tag["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_tag_with_same_name_of_payload)

    def test_update_recipe_removing_tags(self):
        recipe = generate_sample_recipe(user=self.user, with_nested_fields=True)

        payload = {"tags": []}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.tags.count(), 0)


class UpdateRecipeWithIngredientsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_update_recipe_adding_ingredients(self):
        recipe = generate_sample_recipe(user=self.user)

        payload = {"ingredients": [{"name": "New Ingredient"}]}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.ingredients.count(), len(payload["ingredients"]))

        for ingredient in payload["ingredients"]:
            exists_ingredient_with_same_name_of_payload = recipe.ingredients.filter(
                name=ingredient["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_ingredient_with_same_name_of_payload)

    def test_update_recipe_changing_ingredients(self):
        recipe = generate_sample_recipe(user=self.user, with_nested_fields=True)

        payload = {"ingredients": [{"name": "New Ingredient"}]}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.ingredients.count(), len(payload["ingredients"]))

        for ingredient in payload["ingredients"]:
            exists_ingredient_with_same_name_of_payload = recipe.ingredients.filter(
                name=ingredient["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_ingredient_with_same_name_of_payload)

    def test_update_recipe_removing_ingredients(self):
        recipe = generate_sample_recipe(user=self.user, with_nested_fields=True)

        payload = {"ingredients": []}

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.ingredients.count(), 0)


class DeleteRecipeApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_delete_recipe_happy_path(self):
        recipe = generate_sample_recipe(user=self.user)

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_not_delete_recipe_of_other_user(self):
        other_user = generate_sample_user()
        recipe = generate_sample_recipe(user=other_user)

        url = generate_url_to_recipe_detail(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
