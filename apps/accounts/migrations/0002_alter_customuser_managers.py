# Generated by Django 3.2.8 on 2021-11-08 14:21

import apps.accounts.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', apps.accounts.managers.CustomUserManager()),
            ],
        ),
    ]
