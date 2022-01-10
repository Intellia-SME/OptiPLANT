from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class CustomUserManagerTests(TestCase):
    def test_get_by_natural_key_returns_case_insensitive(self):
        user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        self.assertIsNotNone(UserModel._default_manager.get_by_natural_key(user.username.upper()))

    def test_can_create_user_without_password(self):
        UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        self.assertEqual(UserModel.objects.count(), 1)
