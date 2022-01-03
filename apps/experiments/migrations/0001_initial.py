# Generated by Django 3.2.8 on 2021-12-29 10:47

import uuid

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import apps.experiments.utils
import apps.experiments.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                (
                    'dataset',
                    models.FileField(
                        upload_to=apps.experiments.utils.file_directory_path,
                        validators=[
                            apps.experiments.validators.validate_size,
                            django.core.validators.FileExtensionValidator(allowed_extensions=['csv']),
                        ],
                    ),
                ),
                (
                    'experimenter',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='experiments',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]