from random import randint

from core.models import Ingredient, Recipe, Tag
from django.forms.models import model_to_dict
from django.urls import reverse
from recipes.serializers import RecipesSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_ingredient import generate_sample_ingredient
from shared.tests.utils.generate_recipe import generate_sample_recipe, generate_sample_recipe_payload
from shared.tests.utils.generate_tag import generate_sample_tag
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


class CreateRecipeWithTagsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_create_recipe_with_new_tags(self):
        payload = generate_sample_recipe_payload(with_nested_fields=True)

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.tags.count(), len(payload["tags"]))

        for tag in payload["tags"]:
            exists_tag_with_same_name_of_payload = recipe.tags.filter(
                name=tag["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_tag_with_same_name_of_payload)

    def test_create_recipe_with_existing_tags(self):
        payload = generate_sample_recipe_payload()

        existing_tag = Tag.objects.create(user=self.user, name="Existing Tag")
        payload["tags"] = [{"name": existing_tag.name}]

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.tags.count(), len(payload["tags"]))

        self.assertIn(existing_tag, recipe.tags.all())

        for tag in payload["tags"]:
            exists_tag_with_same_name_of_payload = recipe.tags.filter(
                name=tag["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_tag_with_same_name_of_payload)

    def test_create_recipe_with_either_existing_and_new_tags(self):
        payload = generate_sample_recipe_payload()

        existing_tag = Tag.objects.create(user=self.user, name="Existing Tag")
        payload["tags"] = [{"name": existing_tag.name}, {"name": "New Tag"}]

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.tags.count(), len(payload["tags"]))

        self.assertIn(existing_tag, recipe.tags.all())

        for tag in payload["tags"]:
            exists_tag_with_same_name_of_payload = recipe.tags.filter(
                name=tag["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_tag_with_same_name_of_payload)


class CreateRecipeWithIngredientsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_create_recipe_with_new_ingredients(self):
        payload = generate_sample_recipe_payload(with_nested_fields=True)

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.ingredients.count(), len(payload["ingredients"]))

        for ingredient in payload["ingredients"]:
            exists_ingredient_with_same_name_of_payload = recipe.ingredients.filter(
                name=ingredient["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_ingredient_with_same_name_of_payload)

    def test_create_recipe_with_existing_ingredients(self):
        payload = generate_sample_recipe_payload()

        existing_ingredient = Ingredient.objects.create(user=self.user, name="Existing Ingredient")
        payload["ingredients"] = [{"name": existing_ingredient.name}]

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.ingredients.count(), len(payload["ingredients"]))

        self.assertIn(existing_ingredient, recipe.ingredients.all())

        for ingredient in payload["ingredients"]:
            exists_ingredient_with_same_name_of_payload = recipe.ingredients.filter(
                name=ingredient["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_ingredient_with_same_name_of_payload)

    def test_create_recipe_with_either_existing_and_new_ingredients(self):
        payload = generate_sample_recipe_payload()

        existing_ingredient = Ingredient.objects.create(user=self.user, name="Existing Ingredient")
        payload["ingredients"] = [{"name": existing_ingredient.name}, {"name": "New Ingredient"}]

        res = self.client.post(RECIPES_INDEX_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]
        self.assertEqual(recipe.ingredients.count(), len(payload["ingredients"]))

        self.assertIn(existing_ingredient, recipe.ingredients.all())

        for ingredient in payload["ingredients"]:
            exists_ingredient_with_same_name_of_payload = recipe.ingredients.filter(
                name=ingredient["name"],
                user=self.user,
            ).exists()

            self.assertTrue(exists_ingredient_with_same_name_of_payload)


class ListRecipesApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_list_recipes_happy_path(self):
        random_quantity = randint(2, 5)
        for _ in range(random_quantity):
            generate_sample_recipe(user=self.user)

        res = self.client.get(RECIPES_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        existing_recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipesSerializer(existing_recipes, many=True)
        self.assertEqual(res.data["results"], serializer.data)

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
        self.assertEqual(res.data["results"], serializer.data)


class ListRecipesFilteredApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_recipe_list_filtered_by_tags(self):
        tag_to_be_filtered = generate_sample_tag(user=self.user, name="Vegan")
        recipe_to_be_filtered = generate_sample_recipe(
            user=self.user, title="Thai Vegetable Curry", tags=[model_to_dict(tag_to_be_filtered, fields="id")]
        )

        tag_to_not_be_filtered = generate_sample_tag(user=self.user, name="Vegetarian")
        recipe_to_not_be_filtered = generate_sample_recipe(
            user=self.user, title="Aubergine with Tahini", tags=[model_to_dict(tag_to_not_be_filtered, fields="id")]
        )

        recipe_without_any_tag = generate_sample_recipe(user=self.user, title="Fish and chips")

        params = {"tags": f"{tag_to_be_filtered.id}"}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_filtered = RecipesSerializer(recipe_to_be_filtered).data
        self.assertIn(serialized_recipe_to_be_filtered, res.data["results"])

        serialized_recipe_to_not_be_filtered = RecipesSerializer(recipe_to_not_be_filtered).data
        self.assertNotIn(serialized_recipe_to_not_be_filtered, res.data["results"])

        serialized_recipe_without_any_tag = RecipesSerializer(recipe_without_any_tag).data
        self.assertNotIn(serialized_recipe_without_any_tag, res.data["results"])

    def test_recipe_list_filtered_by_ingredients(self):
        ingredient_to_be_filtered = generate_sample_ingredient(user=self.user, name="Cheese")
        recipe_to_be_filtered = generate_sample_recipe(
            user=self.user,
            title="Thai Vegetable Curry",
            ingredients=[model_to_dict(ingredient_to_be_filtered, fields="id")],
        )

        ingredient_to_not_be_filtered = generate_sample_ingredient(user=self.user, name="Chicken")
        recipe_to_not_be_filtered = generate_sample_recipe(
            user=self.user,
            title="Aubergine with Tahini",
            ingredients=[model_to_dict(ingredient_to_not_be_filtered, fields="id")],
        )

        recipe_without_any_ingredient = generate_sample_recipe(user=self.user, title="Fish and chips")

        params = {"ingredients": f"{ingredient_to_be_filtered.id}"}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_filtered = RecipesSerializer(recipe_to_be_filtered).data
        self.assertIn(serialized_recipe_to_be_filtered, res.data["results"])

        serialized_recipe_to_not_be_filtered = RecipesSerializer(recipe_to_not_be_filtered).data
        self.assertNotIn(serialized_recipe_to_not_be_filtered, res.data["results"])

        serialized_recipe_without_any_ingredient = RecipesSerializer(recipe_without_any_ingredient).data
        self.assertNotIn(serialized_recipe_without_any_ingredient, res.data["results"])

    def test_recipe_list_filtered_by_title(self):
        recipe_to_be_filtered = generate_sample_recipe(user=self.user, title="Thai Vegetable Curry")
        recipe_to_not_be_filtered = generate_sample_recipe(user=self.user, title="Aubergine with Tahini")

        params = {"title": recipe_to_be_filtered.title}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_filtered = RecipesSerializer(recipe_to_be_filtered).data
        self.assertIn(serialized_recipe_to_be_filtered, res.data["results"])

        serialized_recipe_to_not_be_filtered = RecipesSerializer(recipe_to_not_be_filtered).data
        self.assertNotIn(serialized_recipe_to_not_be_filtered, res.data["results"])

    def test_recipe_list_filtered_by_price(self):
        recipe_to_be_filtered = generate_sample_recipe(user=self.user, price=10)
        recipe_to_not_be_filtered = generate_sample_recipe(user=self.user, price=20)

        params = {"price_gte": recipe_to_be_filtered.price - 1, "price_lte": recipe_to_be_filtered.price + 1}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_filtered = RecipesSerializer(recipe_to_be_filtered).data
        self.assertIn(serialized_recipe_to_be_filtered, res.data["results"])

        serialized_recipe_to_not_be_filtered = RecipesSerializer(recipe_to_not_be_filtered).data
        self.assertNotIn(serialized_recipe_to_not_be_filtered, res.data["results"])

    def test_recipe_list_filtered_by_time_to_make_in_minutes(self):
        recipe_to_be_filtered = generate_sample_recipe(user=self.user, time_to_make_in_minutes=10)
        recipe_to_not_be_filtered = generate_sample_recipe(user=self.user, time_to_make_in_minutes=20)

        params = {
            "time_to_make_in_minutes_gte": recipe_to_be_filtered.time_to_make_in_minutes - 1,
            "time_to_make_in_minutes_lte": recipe_to_be_filtered.time_to_make_in_minutes + 1,
        }
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_filtered = RecipesSerializer(recipe_to_be_filtered).data
        self.assertIn(serialized_recipe_to_be_filtered, res.data["results"])

        serialized_recipe_to_not_be_filtered = RecipesSerializer(recipe_to_not_be_filtered).data
        self.assertNotIn(serialized_recipe_to_not_be_filtered, res.data["results"])


class ListRecipesSearchedApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_recipe_list_searched_by_title(self):
        recipe_to_be_searched = generate_sample_recipe(user=self.user, title="Thai Vegetable Curry")
        recipe_to_not_be_searched = generate_sample_recipe(user=self.user, title="Aubergine with Tahini")

        params = {"search": recipe_to_be_searched.title.split(" ")[1]}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_searched = RecipesSerializer(recipe_to_be_searched).data
        self.assertIn(serialized_recipe_to_be_searched, res.data["results"])

        serialized_recipe_to_not_be_searched = RecipesSerializer(recipe_to_not_be_searched).data
        self.assertNotIn(serialized_recipe_to_not_be_searched, res.data["results"])

    def test_recipe_list_searched_by_description(self):
        recipe_to_be_searched = generate_sample_recipe(user=self.user, description="This is a unique description")
        recipe_to_not_be_searched = generate_sample_recipe(user=self.user, description="This is another description")

        params = {"search": "unique"}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_searched = RecipesSerializer(recipe_to_be_searched).data
        self.assertIn(serialized_recipe_to_be_searched, res.data["results"])

        serialized_recipe_to_not_be_searched = RecipesSerializer(recipe_to_not_be_searched).data
        self.assertNotIn(serialized_recipe_to_not_be_searched, res.data["results"])

    def test_recipe_list_searched_by_tag_name(self):
        tag_to_be_searched = generate_sample_tag(user=self.user, name="Vegan")
        recipe_to_be_searched = generate_sample_recipe(
            user=self.user, tags=[model_to_dict(tag_to_be_searched, fields="id")]
        )
        recipe_to_not_be_searched = generate_sample_recipe(user=self.user)

        params = {"search": tag_to_be_searched.name}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_searched = RecipesSerializer(recipe_to_be_searched).data
        self.assertIn(serialized_recipe_to_be_searched, res.data["results"])

        serialized_recipe_to_not_be_searched = RecipesSerializer(recipe_to_not_be_searched).data
        self.assertNotIn(serialized_recipe_to_not_be_searched, res.data["results"])

    def test_recipe_list_searched_by_ingredient_name(self):
        ingredient_to_be_searched = generate_sample_ingredient(user=self.user, name="Cheese")
        recipe_to_be_searched = generate_sample_recipe(
            user=self.user, ingredients=[model_to_dict(ingredient_to_be_searched, fields="id")]
        )
        recipe_to_not_be_searched = generate_sample_recipe(user=self.user)

        params = {"search": ingredient_to_be_searched.name}
        res = self.client.get(RECIPES_INDEX_URL, params)

        serialized_recipe_to_be_searched = RecipesSerializer(recipe_to_be_searched).data
        self.assertIn(serialized_recipe_to_be_searched, res.data["results"])

        serialized_recipe_to_not_be_searched = RecipesSerializer(recipe_to_not_be_searched).data
        self.assertNotIn(serialized_recipe_to_not_be_searched, res.data["results"])


class ListRecipesOrderedApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_recipe_list_ordered_by_title(self):
        generate_sample_recipe(user=self.user, title="Aubergine with Tahini")
        generate_sample_recipe(user=self.user, title="Fish and chips")
        generate_sample_recipe(user=self.user, title="Thai Vegetable Curry")

        # Ascending order
        params = {"ordering": "title"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(Recipe.objects.filter(user=self.user).order_by("title"), many=True).data
        self.assertEqual(res.data["results"], serialized_recipes)

        # Descending order
        params = {"ordering": "-title"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(Recipe.objects.filter(user=self.user).order_by("-title"), many=True).data
        self.assertEqual(res.data["results"], serialized_recipes)

    def test_recipe_list_ordered_by_price(self):
        generate_sample_recipe(user=self.user, price=10)
        generate_sample_recipe(user=self.user, price=20)
        generate_sample_recipe(user=self.user, price=30)

        # Ascending order
        params = {"ordering": "price"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(Recipe.objects.filter(user=self.user).order_by("price"), many=True).data
        self.assertEqual(res.data["results"], serialized_recipes)

        # Descending order
        params = {"ordering": "-price"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(Recipe.objects.filter(user=self.user).order_by("-price"), many=True).data
        self.assertEqual(res.data["results"], serialized_recipes)

    def test_recipe_list_ordered_by_time_to_make_in_minutes(self):
        generate_sample_recipe(user=self.user, time_to_make_in_minutes=10)
        generate_sample_recipe(user=self.user, time_to_make_in_minutes=20)
        generate_sample_recipe(user=self.user, time_to_make_in_minutes=30)

        # Ascending order
        params = {"ordering": "time_to_make_in_minutes"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(
            Recipe.objects.filter(user=self.user).order_by("time_to_make_in_minutes"), many=True
        ).data
        self.assertEqual(res.data["results"], serialized_recipes)

        # Descending order
        params = {"ordering": "-time_to_make_in_minutes"}
        res = self.client.get(RECIPES_INDEX_URL, params)
        serialized_recipes = RecipesSerializer(
            Recipe.objects.filter(user=self.user).order_by("-time_to_make_in_minutes"), many=True
        ).data
        self.assertEqual(res.data["results"], serialized_recipes)
