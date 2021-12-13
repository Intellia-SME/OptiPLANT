import os

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from ..views import LoginView, LogoutView, SignupView

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

    def test_successful_logout(self):
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


class SignupViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/signup/'

    def test_signup_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, SignupView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET, POST')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_signup_redirects_to_profile_page(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'me',
                'email': 'me@example.gr',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_signup_authenticates_user(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.client.post(
            self.url,
            data={
                'username': 'me',
                'email': 'me@example.gr',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_signup_email_is_mandatory(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'me',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(response.context['form'].errors['email'].as_text(), '* This field is required.')

    def test_signup_email_is_unique_and_case_insensitive(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'username': 'another',
                'email': 'Guest@guest.gr',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(
            response.context['form'].errors['email'].as_text(), '* A user with that email address already exists.'
        )

    def test_signup_username_is_case_insensitive(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'username': 'ME',
                'email': 'another@guest.gr',
                'password1': os.environ['TEST_USER_PASS'],
                'password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(
            response.context['form'].errors['username'].as_text(), '* A user with that username already exists.'
        )
