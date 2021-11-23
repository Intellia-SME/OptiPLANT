import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from ..views import LoginView

UserModel = get_user_model()


class LoginViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/login/'

    def test_login_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, LoginView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET, POST')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_login_redirects_to_profile_page(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'username': 'me',
                'password': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_login_username_case_insensitive(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'username': 'ME',
                'password': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_unsuccessful_login_message(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'username': 'Wrong_username',
                'password': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertContains(response, 'Your username and password didn\'t match. Please try again.', 1)
