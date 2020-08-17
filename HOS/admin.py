from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from HOS.models import Hospital
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from django.template.response import TemplateResponse


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {"username": ("first_name", "last_name",)}

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(models.Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "is_active",
    )
    list_filter = ("is_active",)
    ordering = ("-is_active", "name")


@admin.register(models.Report_type)
class Report_typeAdmin(admin.ModelAdmin):
    list_display = (
        "short_name",
        "name",
        "recipients",
        "is_active",
        "send_partial_report",
        "timestamp",
    )
    list_filter = ("is_active",)
    ordering = ("-is_active", "short_name")


@admin.register(models.Email_log)
class Email_logAdmin(admin.ModelAdmin):
    list_display = (
        "date_report_sent_for",
        "date_report_sent",
        "report_type",
        "full_report_sent",
        "partial_report_sent",
    )
    list_filter = ("report_type", "full_report_sent", "partial_report_sent")
    ordering = (
        "date_report_sent_for",
        "date_report_sent",
        "report_type",
    )
    readonly_fields = ("show_url",)

    def show_url(self, instance):
        response = format_html("""<a href={0}>{0}</a>""", "/email/hos/")
        return response

    show_url.short_description = "URL"

    # def neki(self, obj):
    #     return render("HOS_email_template.html", {})

    # def show_report(self, request):
    #     return render(request, "HOS_email_template.html", {"context": self.content})

    # show_report.short_description = "Report preview"


@admin.register(models.ReportHOS)
class ReportHOSAdmin(admin.ModelAdmin):
    list_display_links = ("date_reporting",)
    list_display = (
        "date_reporting",
        "hospital",
        "total_hospitalized",
        "total_hospitalized_ICU",
        "total_released",
        "total_deaths",
        "submitted_by",
    )
    ordering = ("-date_reporting", "hospital")
    exclude = ("submitted_by", "report_type")
    list_filter = ("hospital",)
    date_hierarchy = "date_reporting"

    def save_model(self, request, obj, form, change):
        obj.submitted_by = request.user
        super().save_model(request, obj, form, change)

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ReportHOSAdmin, self).get_form(request, obj, **kwargs)
    #     form.hospital.queryset = Hospital.objects.filter(is_active=True)
    #     return form
