from django.urls import path

from .views import CreateExperimentView

app_name = 'experiments'


urlpatterns = [
    path('create/', CreateExperimentView.as_view(), name='create_experiment'),
]
