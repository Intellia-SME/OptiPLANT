import os

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import SignupForm

UserModel = get_user_model()


class SignupFormTest(TestCase):
    def test_valid_form_creates_user(self):
        form = SignupForm(
            data={
                'username': 'another',
                'email': 'Guest@guest.gr',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            }
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(UserModel.objects.count(), 1)

    def test_email_is_required(self):
        form = SignupForm(
            data={
                'username': 'another',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue('required' in form.errors['email'][0])
