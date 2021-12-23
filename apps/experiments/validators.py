from django.core.exceptions import ValidationError


def validate_size(value):
    """
    Validating experiment.dataset's size to be less than 1MB
    """
    if value.size > 1048576:
        raise ValidationError(
            '%(value)s must be less than 1MB',
            params={'value': value},
        )
