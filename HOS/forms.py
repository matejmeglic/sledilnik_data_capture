from django.forms import ModelForm
from HOS.models import ReportHOS
from datetime import datetime

class ReportHOSForm(ModelForm):
    class Meta:
        model = ReportHOS
        fields = 'date_reporting', 'hospital', 'total_hospitalized', 'total_hospitalized_ICU', 'total_released', 'total_deaths', 'deaths_info', 'remark',
        
