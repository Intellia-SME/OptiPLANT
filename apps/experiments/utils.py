from django.utils import timezone


def file_directory_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/datasets/{username}/{year}/{month}/{id}.csv
    """
    return f"datasets/{instance.experimenter.username}/{timezone.now().date().strftime('%Y/%m')}/{instance.id}.csv"
