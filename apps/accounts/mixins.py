from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url


class RedirectAuthenticatedUserMixin:
    def get_default_redirect_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_default_redirect_url())
        return super().dispatch(request, *args, **kwargs)
