from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


class HomeView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'home.html'
        return 'guest.html'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]
