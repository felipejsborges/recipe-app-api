from random import randint

from core.models import Tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shared.tests.mixins.auth import UserAuthenticatedMixinForTests
from shared.tests.utils.generate_tag import generate_sample_tag, generate_sample_tag_payload
from shared.tests.utils.generate_user import generate_sample_user
from tags.serializers import TagsSerializer

TAGS_INDEX_URL = reverse("tags:tag-list")


class TagsIndexNotAuthenticatedApiTests(APITestCase):
    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=None)

    def test_not_get_unauthenticated(self):
        res = self.client.get(TAGS_INDEX_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_post_unauthenticated(self):
        res = self.client.post(TAGS_INDEX_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class TagsIndexNotAllowedMethodsApiTests(UserAuthenticatedMixinForTests, APITestCase):
#     def test_put_detail_not_allowed(self):
#         res = self.client.put(TAGS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_patch_detail_not_allowed(self):
#         res = self.client.patch(TAGS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_delete_detail_not_allowed(self):
#         res = self.client.delete(TAGS_INDEX_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateTagApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_create_tag_happy_path(self):
        payload = generate_sample_tag_payload(user=self.user)

        res = self.client.post(TAGS_INDEX_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        tag = Tag.objects.get(id=res.data["id"])
        self.assertEqual(tag.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(tag, k), v)


class ListTagsApiTests(UserAuthenticatedMixinForTests, APITestCase):
    def test_list_tags_happy_path(self):
        random_quantity = randint(2, 5)
        for _ in range(random_quantity):
            generate_sample_tag(user=self.user)

        res = self.client.get(TAGS_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        existing_tags = Tag.objects.all().order_by("name")
        serializer = TagsSerializer(existing_tags, many=True)
        self.assertEqual(res.data["results"], serializer.data)

    def test_tag_list_limited_to_user(self):
        random_quantity_linked_to_other_user = randint(1, 3)
        for _ in range(random_quantity_linked_to_other_user):
            other_user = generate_sample_user()
            generate_sample_tag(user=other_user)

        random_quantity = randint(1, 3)
        for _ in range(random_quantity):
            generate_sample_tag(user=self.user)

        res = self.client.get(TAGS_INDEX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.filter(user=self.user).order_by("name")
        serializer = TagsSerializer(tags, many=True)
        self.assertEqual(res.data["results"], serializer.data)
