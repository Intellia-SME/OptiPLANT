import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from .utils import Timestampable, file_directory_path
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
