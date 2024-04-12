from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.utils.generate_user import generate_sample_user, generate_sample_user_payload

USERS_TOKENS_URL = reverse("users:tokens")


class CreateTokenApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.user_payload = generate_sample_user_payload()

        generate_sample_user(**self.user_payload)

    def test_create_token_happy_path(self):
        request_payload = {
            "email": self.user_payload["email"],
            "password": self.user_payload["password"],
        }
        res = self.client.post(USERS_TOKENS_URL, request_payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_not_create_token_if_password_mismatch(self):
        request_payload = {
            "email": self.user_payload["email"],
            "password": "bad_pass",
        }
        res = self.client.post(USERS_TOKENS_URL, request_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_token_if_email_does_not_exist(self):
        request_payload = {
            "email": "non-existing-email@example.com",
            "password": self.user_payload["password"],
        }
        res = self.client.post(USERS_TOKENS_URL, request_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_token_if_password_is_blank(self):
        request_payload = {
            "email": "non-existing-email@example.com",
            "password": "",
        }
        res = self.client.post(USERS_TOKENS_URL, request_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
