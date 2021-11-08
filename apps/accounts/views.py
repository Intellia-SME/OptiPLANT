from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class LoginView(auth_views.LoginView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
