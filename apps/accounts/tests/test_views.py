import os

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from ..views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)

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


class PasswordResetViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/password-reset/'

    def test_password_reset_view_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, PasswordResetView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET, POST')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_password_reset_redirects_to_password_reset_done(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        response = self.client.post(
            self.url,
            data={
                'email': 'guest@guest.gr',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/password-reset-done/')

    def test_successful_password_reset_sends_email(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        self.client.post(
            self.url,
            data={
                'email': 'guest@guest.gr',
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Password reset", mail.outbox[0].subject)

    def test_wrong_email_does_not_send_email(self):
        UserModel.objects.create_user(username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS'])
        self.client.post(
            self.url,
            data={
                'email': 'wrong@guest.gr',
            },
        )
        self.assertEqual(len(mail.outbox), 0)


class PasswordResetDoneViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/password-reset-done/'

    def test_password_reset_done_view_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, PasswordResetDoneView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')


class PasswordResetConfirmViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/reset/MTc/axc845-b0f523060bb845e91ec34e8e6a9c8658/'

    def test_password_reset_view_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, PasswordResetConfirmView.as_view().__name__)

    def test_http_methods_allowed(self):
        """
        To test the options you need to make two requests, because the first GET request
        """
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response1 = self.client.get('/accounts/reset/' + uid + '/' + token + '/')
        response2 = self.client.options(response1.url)
        self.assertEqual(response2['allow'], 'GET, POST')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')

    def test_successful_password_reset_redirects_to_reset_done(self):
        """
        To test this view you need to make two requests, one GET request with uid and token, and another
        POST request to the url that you are redirected to from the first request
        """
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response1 = self.client.get('/accounts/reset/' + uid + '/' + token + '/')
        response = self.client.post(
            response1.url,
            data={
                'new_password1': os.environ['TEST_USER_PASS'],
                'new_password2': os.environ['TEST_USER_PASS'],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/reset/done/')


class PasswordResetCompleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/accounts/reset/done/'

    def test_password_reset_complete_view_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, PasswordResetCompleteView.as_view().__name__)

    def test_http_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')

    def test_authenticated_user_is_redirected(self):
        user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/profile/')
