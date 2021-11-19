import os

from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class CustomUserManagerTests(TestCase):
    def test_get_by_natural_key_returns_case_insensitive(self):
        user = UserModel.objects.create(
            username="guest", email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.assertIsNotNone(UserModel._default_manager.get_by_natural_key(user.username.upper()))
