from django.urls import path

from .views import LoginView, LogoutView, ProfileView, SignupView

app_name = 'accounts'


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
]
