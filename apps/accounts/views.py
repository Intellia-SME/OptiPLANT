from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    http_method_names = ['get', 'post']
    template_name = 'accounts/login.html'
