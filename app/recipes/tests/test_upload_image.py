import os
import tempfile

from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_recipe import generate_sample_recipe

RECIPES_IMAGE_UPLOAD_URL = "recipes:recipe-image"


def generate_url_to_recipe_image_upload(recipe_id=None):
    return reverse(RECIPES_IMAGE_UPLOAD_URL, args=[recipe_id])


class RecipeImageUploadNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_patch_unauthenticated(self):
        res = self.client.patch(generate_url_to_recipe_image_upload(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeImageUploadNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_post_detail_not_allowed(self):
        res = self.client.post(generate_url_to_recipe_image_upload(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_detail_not_allowed(self):
        res = self.client.get(generate_url_to_recipe_image_upload(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_detail_not_allowed(self):
        res = self.client.put(generate_url_to_recipe_image_upload(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_detail_not_allowed(self):
        res = self.client.delete(generate_url_to_recipe_image_upload(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RecipeImageUploadApiTests(UserAuthenticatedMixinForTests, APITestCase):
    @classmethod
    def setUpTestData(cls):  # pylint: disable=invalid-name
        super().setUpTestData()

        cls.recipe = generate_sample_recipe(user=cls.user)

    @classmethod
    def tearDownTestData(cls):  # pylint: disable=invalid-name
        cls.recipe.image.delete()

        super().tearDownTestData()

    def test_upload_recipe_image_happy_path(self):
        url = generate_url_to_recipe_image_upload(self.recipe.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))

            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = {"image": image_file}
            res = self.client.patch(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.recipe.refresh_from_db()

        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_not_upload_recipe_image_without_an_image(self):
        url = generate_url_to_recipe_image_upload(self.recipe.id)

        payload = {"image": "not_an_image"}

        res = self.client.patch(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
