from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .forms import CreateExperimentForm


class CreateExperimentView(LoginRequiredMixin, CreateView):
    http_method_names = ['get', 'post']
    form_class = CreateExperimentForm
    template_name = 'experiments/create_experiment.html'
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form
