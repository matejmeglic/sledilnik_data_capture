from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404

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
from HOS.models import ReportHOS, Report_type, Hospital, Email_log
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

import logging


@login_required
def hos_report(request, report_id):
    report = get_object_or_404(Email_log, id=report_id)
    email_date = dateformat.format(report.date_report_sent_for, "Y-m-d")
    context = {
        "email_date": email_date,
        "table_content": ReportHOS.objects.filter(date_reporting=email_date),
        "to_emails": report.recipients,
    }

    return render(request, "HOS_email_template.html", {"context": context})

