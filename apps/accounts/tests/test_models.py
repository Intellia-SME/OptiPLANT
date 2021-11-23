import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

UserModel = get_user_model()


class CustomUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create(
            username="guest", email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )

    def test_username_is_mandatory(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(email="guest2@guest.gr", password=self.user.password)
        self.assertEqual(e.exception.messages[0], 'This field cannot be blank.')

    def test_username_is_unique(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(username=self.user.username, email="guest2@guest.gr", password=self.user.password)
        self.assertEqual(e.exception.messages[0], 'A user with that username already exists.')

    def test_username_is_case_insensitive(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(
                username=self.user.username.upper(), email="guest2@guest.gr", password=self.user.password
            )
        self.assertEqual(e.exception.messages[0], 'A user with that username already exists.')

    def test_username_is_not_unicode_based(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(
                username=self.user.username + "¬", email="guest2@guest.gr", password=self.user.password
            )
        self.assertTrue('Enter a valid username.' in e.exception.messages[0])

    def test_email_is_mandatory(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(username="guest1", password=self.user.password)
        self.assertEqual(e.exception.messages[0], 'This field cannot be blank.')

    def test_email_is_unique(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(username="guest2", email=self.user.email, password=self.user.password)
        self.assertEqual(e.exception.messages[0], 'A user with that email address already exists.')

    def test_email_is_case_insensitive(self):
        with self.assertRaises(ValidationError) as e:
            UserModel.objects.create(username="guest2", email=self.user.email.upper(), password=self.user.password)
        self.assertEqual(e.exception.messages[0], 'A user with that email address already exists.')
