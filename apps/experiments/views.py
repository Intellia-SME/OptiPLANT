from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CreateExperimentForm
from .mixins import ObjectOwnershipRequiredMixin
from .models import Experiment


class CreateExperimentView(LoginRequiredMixin, CreateView):
    http_method_names = ['get', 'post']
    form_class = CreateExperimentForm
    template_name = 'experiments/create_experiment.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def get_success_url(self):
        return reverse_lazy('experiments:main_experiment', kwargs={'pk': self.object.id})


class MainExperimentView(LoginRequiredMixin, ObjectOwnershipRequiredMixin, DetailView):
    http_method_names = ['get']
    queryset = Experiment.objects.all()
    template_name = 'experiments/main_experiment.html'
