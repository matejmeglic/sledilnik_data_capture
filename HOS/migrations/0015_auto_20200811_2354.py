# Generated by Django 3.0.8 on 2020-08-11 21:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOS', '0014_auto_20200811_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporthos',
            name='submitted_by',
        ),
        migrations.AlterField(
            model_name='reporthos',
            name='date_reporting',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 23, 54, 59, 725149), verbose_name='Date'),
        ),
    ]
