from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


class Hospital(models.Model):
    name = models.CharField(max_length=100, help_text='Polno ime COVID bolnišnice.')
    short_name = models.CharField(max_length=30, help_text='Kratica COVID bolnišnice.')
    is_active = models.BooleanField(help_text='Ali je bolnišnica trenutno aktivna?', default=False)

    class Meta:
        verbose_name = "Bolnica"
        verbose_name_plural = "Bolnice"
        ordering = ('-is_active', 'name')

    def __str__(self):
        return self.short_name


class ReportHOS(models.Model):
    date_form_saved = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date_reporting = models.DateField(("Date"), default=django.utils.timezone.now, help_text="LLLL-MM-DD")
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    total_hospitalized = models.PositiveIntegerField(null=True, blank=True, help_text='Število vseh hospitaliziranih COVID')
    total_hospitalized_ICU = models.PositiveIntegerField(null=True, blank=True, help_text='Število hospitaliziranih COVID na intenzivni negi')
    total_released = models.PositiveIntegerField('Število odpuščenih COVID', null=True, blank=True)
    total_deaths = models.PositiveIntegerField(null=True, blank=True, help_text='Število smrtnih primerov s COVID')
    deaths_info = models.CharField('Informacije o smrti', max_length=100, help_text='Spol M/Ž in starost umrlih, npr. M70 Ž85', blank=True, null=True)
    remark = models.TextField('Opombe', blank=True, null=True)

    class Meta:
        verbose_name = "Poročilo bolnice"
        verbose_name_plural = "Poročila bolnic"
        ordering = ('-date_reporting', 'hospital')

    def __str__(self):
        return str(self.date_form_saved)
