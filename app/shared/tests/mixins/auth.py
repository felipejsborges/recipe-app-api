from shared.tests.utils.generate_user import generate_sample_user


class UserAuthenticatedMixinForTests(object):
    @classmethod
    def setUpTestData(cls):  # pylint: disable=invalid-name
        super().setUpTestData()

        cls.user = generate_sample_user()

    def setUp(self):  # pylint: disable=invalid-name
        super().setUp()

        self.client.force_authenticate(user=self.user)
