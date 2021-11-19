from django.conf import settings

from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect


class LogoutView(auth_views.LogoutView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.next = settings.CUSTOM_LOGOUT_REDIRECT_URL
        return HttpResponseRedirect(self.next)
