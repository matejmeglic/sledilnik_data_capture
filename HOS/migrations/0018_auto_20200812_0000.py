# Generated by Django 3.0.8 on 2020-08-11 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOS', '0017_auto_20200811_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthos',
            name='date_reporting',
            field=models.DateField(default=datetime.datetime(2020, 8, 12, 0, 0, 33, 236347), verbose_name='Date'),
        ),
    ]
