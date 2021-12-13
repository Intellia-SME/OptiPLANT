from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import SignupForm


class SignupView(FormView):
    http_method_names = ['get', 'post']
    form_class = SignupForm
    redirect_authenticated_user = True
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class LoginView(auth_views.LoginView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.next = settings.CUSTOM_LOGOUT_REDIRECT_URL
        return HttpResponseRedirect(self.next)


class PasswordResetView(auth_views.PasswordResetView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    subject_template_name = 'accounts/password_reset_email/password_reset_subject.txt'
    email_template_name = 'accounts/password_reset_email/password_reset_body.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'accounts/password_reset.html'

    def get_default_redirect_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_default_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    http_method_names = ['get']
    redirect_authenticated_user = True
    template_name = 'accounts/password_reset_done.html'

    def get_default_redirect_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_default_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

    def get_default_redirect_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_default_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    http_method_names = ['get']
    redirect_authenticated_user = True
    template_name = 'accounts/password_reset_complete.html'

    def get_default_redirect_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_default_redirect_url())
        return super().dispatch(request, *args, **kwargs)
