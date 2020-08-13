from django import forms
from django.forms import ModelForm
from HOS.models import ReportHOS

from .models import Hospital


class ReportHOSForm(ModelForm):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.filter(is_active=True))

    class Meta:
        model = ReportHOS
        exclude = ('date_form_saved', 'submitted_by')
