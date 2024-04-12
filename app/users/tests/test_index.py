from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.utils.generate_user import generate_sample_user, generate_sample_user_payload

USERS_INDEX_URL = reverse("users:index")


class CreateUserApiTests(APITestCase):
    def test_create_user(self):
        payload = generate_sample_user_payload()
        res = self.client.post(USERS_INDEX_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_not_create_user_with_email_that_already_exists(self):
        payload = generate_sample_user_payload()
        generate_sample_user(**payload)
        res = self.client.post(USERS_INDEX_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
