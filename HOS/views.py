from django.shortcuts import render
from django.shortcuts import redirect

from .forms import ReportHOSForm
from .models import Report_type


def index(request):
    return render(request, "index.html", {})


def hos_form(request):

    if request.method == "POST":
        form = ReportHOSForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.submitted_by = request.user
            report.report_type = "HOS"
            report.save()
            return render(request, "HOS_form_confirmation.html", {"report": report})
    else:
        form = ReportHOSForm()

    return render(request, "HOS_form.html", {"form": form})


from django_docopt_command import DocOptCommand
from django.utils import timezone, dateformat
from HOS.models import ReportHOS, Report_type, Hospital, Email, Timeline
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

import logging


def hos_report(request):
    queryset = ReportHOS.objects.all()
    queryset_hospitals = Hospital.objects.filter(is_active=True)
    yesterday = dateformat.format(
        datetime.datetime.utcnow().date() - datetime.timedelta(days=1), "Y-m-d"
    )

    list_hospitals = []
    for hospital in queryset_hospitals:
        list_hospitals.append(hospital.short_name)

    for report in queryset:
        if dateformat.format(report.date_reporting, "Y-m-d") == yesterday:
            for hospital in queryset_hospitals:
                if report.hospital == hospital:
                    list_hospitals.remove(hospital.short_name)

    if len(list_hospitals) == 0:

        email_date = dateformat.format(
            datetime.datetime.utcnow().date() - datetime.timedelta(days=1), "d.m.Y"
        )
        table_content = []

        for report in queryset:
            if dateformat.format(report.date_reporting, "Y-m-d") == yesterday:
                table_content.append(report)

        context = {
            "email_date": email_date,
            "table_content": table_content,
        }

        return render(request, "HOS_email_template.html", context)

