from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import DetailView

from apps.mlcore.utils import get_experiment_statistics

from .mixins import ObjectOwnershipRequiredMixin
from .models import Experiment


class JSONExperimentStatisticsView(LoginRequiredMixin, ObjectOwnershipRequiredMixin, DetailView):
    http_method_names = ['get']
    model = Experiment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        statistics = get_experiment_statistics(self.object)
        return JsonResponse(statistics, safe=False)
