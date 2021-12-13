import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.views.generic import TemplateView

from ..mixins import RedirectAuthenticatedUserMixin

UserModel = get_user_model()


class RedirectAuthenticatedUserMixinTests(TestCase):
    class DummyView(RedirectAuthenticatedUserMixin, TemplateView):
        template_name = 'dummy.html'
        pass

    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().get('/')
        cls.user = UserModel.objects.create_user(
            username='me', email="guest@guest.gr", password=os.environ['TEST_USER_PASS']
        )

    def test_get_default_redirect_url_is_login_redirect_url(self):
        self.assertEqual(self.DummyView().get_default_redirect_url(), '/accounts/profile/')

    def test_mixin_authenticated_user_is_redirected(self):
        self.request.user = self.user
        response = self.DummyView.as_view()(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/profile/')

    def test_mixin_anonymous_not_redirected(self):
        self.request.user = AnonymousUser()
        response = self.DummyView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
