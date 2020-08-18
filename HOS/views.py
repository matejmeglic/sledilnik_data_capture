from HOS.management.commands.report import send_email_hos
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import dateformat

from .management.commands.report import send_email_hos
from HOS.models import ReportHOS, Email_log
from .forms import ReportHOSForm


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

            send_email_hos()  # currently triggers email sending

            return render(request, "HOS_form_confirmation.html", {"report": report})

    else:
        form = ReportHOSForm()

    return render(request, "HOS_form.html", {"form": form})


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

