from django.db import models
from django.utils import timezone


class Timestampable(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def file_directory_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/datasets/{username}/{year}/{month}/{id}.csv
    """
    return f"datasets/{instance.experimenter.username}/{timezone.now().date().strftime('%Y/%m')}/{instance.id}.csv"
