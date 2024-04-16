from core.models import Tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_tag import generate_sample_tag
from shared.tests.utils.generate_user import generate_sample_user
from tags.serializers import TagsSerializer

TAGS_DETAIL_URL = "tags:tag-detail"


def generate_url_to_tag_detail(tag_id=None):
    return reverse(TAGS_DETAIL_URL, args=[tag_id])


class TagDetailNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(generate_url_to_tag_detail())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_put_unauthenticated(self):
        res = self.client.put(generate_url_to_tag_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_patch_unauthenticated(self):
        res = self.client.patch(generate_url_to_tag_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_delete_unauthenticated(self):
        res = self.client.delete(generate_url_to_tag_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TagDetailNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_post_detail_not_allowed(self):
        res = self.client.post(generate_url_to_tag_detail(), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetTagApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_get_tag_happy_path(self):
        tag = generate_sample_tag(user=self.user)

        url = generate_url_to_tag_detail(tag.id)
        res = self.client.get(url)

        serializer = TagsSerializer(tag)
        self.assertEqual(res.data, serializer.data)


class UpdateTagApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_full_update(self):
        tag = generate_sample_tag(user=self.user)

        payload = {
            "name": "New tag name",
        }

        url = generate_url_to_tag_detail(tag.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(tag, k), v)
        self.assertEqual(tag.user, self.user)

    def test_update_tag_user_fails(self):
        tag = generate_sample_tag(user=self.user)

        other_user = generate_sample_user()
        payload = {"user": other_user.id}

        url = generate_url_to_tag_detail(tag.id)
        self.client.patch(url, payload)

        tag.refresh_from_db()

        self.assertEqual(tag.user, self.user)


class DeleteTagApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_delete_tag_happy_path(self):
        tag = generate_sample_tag(user=self.user)

        url = generate_url_to_tag_detail(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())

    def test_not_delete_tag_of_other_user(self):
        other_user = generate_sample_user()
        tag = generate_sample_tag(user=other_user)

        url = generate_url_to_tag_detail(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tag.objects.filter(id=tag.id).exists())
