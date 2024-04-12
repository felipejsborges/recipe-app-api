from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests

USERS_DETAIL_URL = reverse("users:details")


class UserDetailNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(USERS_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_put_unauthenticated(self):
        res = self.client.put(USERS_DETAIL_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_post_detail_not_allowed(self):
        res = self.client.post(USERS_DETAIL_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_detail_not_allowed(self):
        res = self.client.patch(USERS_DETAIL_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_detail_not_allowed(self):
        res = self.client.delete(USERS_DETAIL_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetUserApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_get_user_happy_path(self):
        res = self.client.get(USERS_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"email": self.user.email, "name": self.user.name})


class UpdateUserApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_update_user_happy_path(self):
        payload = {"name": "Updated name", "email": "updated@email.com", "password": "new_password_123"}

        res = self.client.put(USERS_DETAIL_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
