from django import forms

from .models import Experiment


class CreateExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['name', 'description', 'dataset']

    def save(self, commit=True):
        self.instance.experimenter = self.request.user
        return super().save(commit=commit)
