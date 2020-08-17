from django_docopt_command import DocOptCommand
from django.utils import timezone, dateformat
from HOS.models import ReportHOS, Report_type, Hospital, Email_log
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import logging

logger = logging.getLogger("management.commands")


DOCS = """
Usage:
    report list [--count=<n>]
    report [--traceback] hos_report
    report email

Options:
    -h --help     Show this screen.
    --version     Show version.
"""


class Command(DocOptCommand):
    docs = DOCS

    def handle_docopt(self, args):
        if args["list"]:
            list_reports(count=int(args["--count"]))
        if args["hos_report"]:
            hos_report()


def list_reports(count=None):
    queryset = ReportHOS.objects.all()
    if count:
        queryset = queryset[:count]
    for report in queryset:
        logger.info(
            "{} - {} - {}".format(
                report.date_reporting, report.hospital.short_name, report.submitted_by
            )
        )


def hos_report():
    email_date = dateformat.format(
        datetime.datetime.utcnow().date() - datetime.timedelta(days=1), "Y-m-d"
    )  # hardcoded as yesterday

    # get active hospitals
    list_hospitals = []
    for hospital in Hospital.objects.filter(is_active=True):
        list_hospitals.append(hospital.short_name)

    # which hospitals already reported
    for report in ReportHOS.objects.all():
        if dateformat.format(report.date_reporting, "Y-m-d") == email_date:
            for hospital in Hospital.objects.filter(is_active=True):
                if report.hospital == hospital:
                    if str(hospital.short_name) in list_hospitals:
                        list_hospitals.remove(hospital.short_name)

    # if all active hospitals already reported, send email
    if len(list_hospitals) == 0:
        email_date_formatted = dateformat.format(
            datetime.datetime.utcnow().date() - datetime.timedelta(days=1), "d. m. Y"
        )
        context = {
            "email_date": email_date_formatted,
            "table_content": ReportHOS.objects.filter(date_reporting=email_date),
        }

        report_object = Report_type.objects.get(slug="HOS")
        email_list = report_object.recipients.all()
        to_emails = []
        for email in email_list:
            to_emails.append(email.email)
        html_content = render_to_string("HOS_email_template.html", {"context": context})

        saved_report = Email_log()
        saved_report.date_report_sent = datetime.datetime.utcnow().date()
        saved_report.date_report_sent_for = email_date
        saved_report.report_type = report_object
        saved_report.full_report_sent = True
        saved_report.partial_report_sent = False
        saved_report.recipients = to_emails
        saved_report.save()

        message = Mail(
            from_email="info@sledilnik.org",
            to_emails=to_emails,
            subject="HOS: Poročilo o stanju COVID pacientov v bolnišnicah na dan {}.".format(
                email_date_formatted
            ),
            html_content=html_content,
        )
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)

        except Exception as e:
            print(e)
        logger.info("EMAIL WOULD BE SENT NORMALLY.")

    # if not every active hospital reports is gathered,
    # but time for partial email send was already reached, send partial email
    else:
        logger.info(
            "Email ne bo poslan ker bolnišnice {} še niso poslale podatkov.".format(
                list_hospitals
            )
        )

