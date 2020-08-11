"""Models"""

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ReportHOS(models.Model):
    """Model representing a HOS entry."""
    date_form_saved = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_reporting = models.DateField(("Date"), default=datetime.now())
    hospital = models.ForeignKey('Hospital', on_delete=models.SET_NULL, null=True)
    total_hospitalized = models.IntegerField(default=0, help_text='Število vseh hospitaliziranih COVID')
    total_hospitalized_ICU = models.IntegerField(default=0, help_text='Število hospitaliziranih COVID na intenzivni negi')
    total_released = models.IntegerField(default=0, help_text='Število odpuščenih COVID')
    total_deaths = models.IntegerField(default=0, help_text='Število smrtnih primerov s COVID')
    deaths_info = models.CharField(max_length=100, help_text='Spol M/Ž in starost umrlih, npr. M70 Ž85', blank=True, null=True)
    remark = models.CharField(max_length=100, help_text='Opomba, pojasnilo', blank=True, null=True)
    def __str__(self):
        """Return better info to admin panel"""
        return str(self.date_form_saved)


class Hospital(models.Model):
    """Model representing active hospitals."""
    name = models.CharField(max_length=35, help_text='Polno ime COVID bolnišnice.')
    short_name = models.CharField(max_length=10, help_text='Kratica COVID bolnišnice.')
    is_active = models.BooleanField(help_text='Ali je bolnišnica trenutno aktivna?', default=False)
    def __str__(self):
        """Return better info to admin panel"""
        return self.short_name

