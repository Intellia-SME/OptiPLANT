import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.constants import MAX_DATASET_SIZE, MAX_TRAINING_COST
from apps.core.models import Timestampable

from .utils import file_directory_path
from .validators import validate_size


class Experiment(Timestampable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experimenter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="experiments", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    dataset = models.FileField(
        upload_to=file_directory_path, validators=[validate_size, FileExtensionValidator(allowed_extensions=['csv'])]
    )

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def training_cost(self):
        if self.dataset.size > MAX_DATASET_SIZE / 2:
            return MAX_TRAINING_COST
        return MAX_TRAINING_COST / 2
