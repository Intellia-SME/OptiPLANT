from django.urls import path

from .json_views import JSONExperimentStatisticsView
from .views import CreateExperimentView, MainExperimentView

app_name = 'experiments'


urlpatterns = [
    path('create/', CreateExperimentView.as_view(), name='create_experiment'),
    path('<uuid:pk>/main/', MainExperimentView.as_view(), name='main_experiment'),
    path('<uuid:pk>/main/get-statistics/', JSONExperimentStatisticsView.as_view(), name='json_statistics'),
]
