from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    http_method_names = ['get', 'post']
    # TODO: After home page creation
    # redirect_authenticated_user = True
    template_name = 'accounts/login.html'
