from django.core.exceptions import ValidationError

from apps.core.constants import MAX_DATASET_SIZE


def validate_size(value):
    """
    Validating experiment.dataset's size to be less than 1MB
    """
    if value.size > MAX_DATASET_SIZE:
        raise ValidationError(
            '%(value)s must be less than 1MB',
            params={'value': value},
        )
