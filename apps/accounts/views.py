from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import SignupForm
from .mixins import RedirectAuthenticatedUserMixin


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


class PasswordResetView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetView):
    http_method_names = ['get', 'post']
    subject_template_name = 'accounts/password_reset_email/password_reset_subject.txt'
    email_template_name = 'accounts/password_reset_email/password_reset_body.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'accounts/password_reset.html'


class PasswordResetDoneView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetDoneView):
    http_method_names = ['get']
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetConfirmView):
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetCompleteView(RedirectAuthenticatedUserMixin, auth_views.PasswordResetCompleteView):
    http_method_names = ['get']
    template_name = 'accounts/password_reset_complete.html'
