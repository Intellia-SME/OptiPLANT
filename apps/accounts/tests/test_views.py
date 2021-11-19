import os

from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import resolve

from ..views import LogoutView

UserModel = get_user_model()


class LogoutViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/logout/'

    def test_logout_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, LogoutView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'POST')

    def test_successful_logout_(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.client.post(self.url)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_logout_redirects_to_homepage(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        # TODO self.assertRedirects(response, '/')
