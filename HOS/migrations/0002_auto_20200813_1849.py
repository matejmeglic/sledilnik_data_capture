# Generated by Django 3.1 on 2020-08-13 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthos',
            name='total_deaths',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Število smrtnih primerov s COVID'),
        ),
        migrations.AlterField(
            model_name='reporthos',
            name='total_hospitalized',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Število vseh hospitaliziranih COVID'),
        ),
        migrations.AlterField(
            model_name='reporthos',
            name='total_hospitalized_ICU',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Število hospitaliziranih COVID na intenzivni negi'),
        ),
    ]
