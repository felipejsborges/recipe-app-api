from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_INDEX_URL = reverse("users:index")


def _generate_sample_user_payload(**params):
    return {"email": "test@example.com", "password": "test_pass_123", "name": "Test Name", **params}


def _generate_sample_user(**params):
    return get_user_model().objects.create(**{**_generate_sample_user_payload(), **params})


class UsersPublicRoutesApiTests(TestCase):
    def setUp(self):  # pylint: disable=invalid-name
        self.client = APIClient()

    def test_create_user(self):
        payload = _generate_sample_user_payload()
        res = self.client.post(USER_INDEX_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_not_create_user_with_email_that_already_exists(self):
        payload = _generate_sample_user_payload()
        _generate_sample_user(**payload)
        res = self.client.post(USER_INDEX_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
