from django.contrib import admin
from . import models

<<<<<<< HEAD
=======

>>>>>>> 53ff0b61ab45b4d824041869d3a70fc388e32b20
@admin.register(models.Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active',)
    list_filter = ('is_active',)
    ordering = ('-is_active', 'name')


@admin.register(models.ReportHOS)
class ReportHOSAdmin(admin.ModelAdmin):
    list_display_links = ('date_reporting',)
<<<<<<< HEAD
    list_display = ('date_reporting', 'hospital', 'total_hospitalized', 'total_hospitalized_ICU', 'total_released', 'total_deaths', 'submitted_by')
=======
    list_display = ('submitted_by', 'date_reporting', 'hospital', 'total_hospitalized',
                    'total_hospitalized_ICU', 'total_released', 'total_deaths')
>>>>>>> 53ff0b61ab45b4d824041869d3a70fc388e32b20
    ordering = ('-date_reporting', 'hospital')
    exclude = ('submitted_by',)
    list_filter = ("hospital",)
    date_hierarchy = "date_reporting"

    def save_model(self, request, obj, form, change):
        obj.submitted_by = request.user
        super().save_model(request, obj, form, change)
