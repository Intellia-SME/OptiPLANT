from django.urls import path

from .views import CreateExperimentView, MainExperimentView

app_name = 'experiments'


urlpatterns = [
    path('create/', CreateExperimentView.as_view(), name='create_experiment'),
    path('<uuid:pk>/main/', MainExperimentView.as_view(), name='main_experiment'),
]
