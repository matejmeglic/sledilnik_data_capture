# Generated by Django 3.0.8 on 2020-08-11 20:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HOS', '0008_auto_20200811_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthos',
            name='date_reporting',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 22, 40, 44, 157105), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='reporthos',
            name='submitted_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
