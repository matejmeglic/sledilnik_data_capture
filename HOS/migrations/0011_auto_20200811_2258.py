# Generated by Django 3.0.8 on 2020-08-11 20:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOS', '0010_auto_20200811_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthos',
            name='date_reporting',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 22, 58, 7, 455031), verbose_name='Date'),
        ),
    ]
