"""Forms"""
from django.forms import ModelForm
from HOS.models import ReportHOS

class ReportHOSForm(ModelForm):
    """HOS input form - ReportHOS model"""
    class Meta:
        model = ReportHOS
        fields = 'date_reporting', 'hospital', 'total_hospitalized', 'total_hospitalized_ICU', 'total_released', 'total_deaths', 'deaths_info', 'remark',   
