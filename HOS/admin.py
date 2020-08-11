"""Admin"""

from django.contrib import admin

# Register your models here.

from .models import ReportHOS, Hospital

class HospitalAdmin(admin.ModelAdmin):
    """Display Hospitals on Admin panel"""
    list_display = ('name', 'short_name', 'is_active',)
    ordering = ('-is_active', 'name')

class ReportHOSAdmin(admin.ModelAdmin):
    """Display Hospitals on Admin panel"""
    list_display = ('id', 'submitted_by', 'date_reporting', 'hospital', 'total_hospitalized',
                    'total_hospitalized_ICU', 'total_released', 'total_deaths')
    ordering = ('-date_reporting', 'hospital')
    exclude = ['submitted_by',]
    def save_model(self, request, obj, form, change):
        obj.submitted_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(ReportHOS, ReportHOSAdmin)
