from core import models
from django.test import TestCase
from shared.tests.utils.generate_user import generate_sample_user


class TagModelTests(TestCase):
    def test_create_tag(self):
        user = generate_sample_user()

        tag = models.Tag.objects.create(
            user=user,
            name="Sample tag",
        )

        self.assertEqual(str(tag), tag.name)
