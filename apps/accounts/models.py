from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )

    objects = CustomUserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()
        self.username = self.username.lower()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
