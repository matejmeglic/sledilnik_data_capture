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
    report hos_report
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
    queryset = ReportHOS.objects.all()
    queryset_hospitals = Hospital.objects.filter(is_active=True)
    email_date = dateformat.format(
        datetime.datetime.utcnow().date() - datetime.timedelta(days=1), "Y-m-d"
    )  # hardcoded

    # get active hospitals
    list_hospitals = []
    for hospital in queryset_hospitals:
        list_hospitals.append(hospital.short_name)

    # get reports for reporting day [currently hardcoded to -1d]
    for report in queryset:
        if dateformat.format(report.date_reporting, "Y-m-d") == email_date:
            for hospital in queryset_hospitals:
                if report.hospital == hospital:
                    list_hospitals.remove(hospital.short_name)

    # if all active hospitals already reported, send email
    if len(list_hospitals) == 0:

        table_content = []
        report_type = ""
        for report in queryset:
            if dateformat.format(report.date_reporting, "Y-m-d") == email_date:
                table_content.append(report)
                report_type = report.report_type

        context = {
            "email_date": email_date,
            "table_content": table_content,
        }

        report_type_object = Report_type.objects.filter(short_name=report_type)
        to_emails = report_type_object[0].recipients.splitlines()
        html_content = render_to_string("HOS_email_template.html", {"context": context})

        # logger.info(render_to_string("HOS_email_template.html", {"context": context}))

        saved_report = Email_log()
        saved_report.date_report_sent = datetime.datetime.utcnow().date()
        saved_report.date_report_sent_for = email_date
        saved_report.report_type = report_type_object[0]  # hackish
        saved_report.full_report_sent = True
        saved_report.partial_report_sent = False
        saved_report.recipients = to_emails
        saved_report.content = context
        saved_report.save()

        # message = Mail(
        #     from_email="info@sledilnik.org",
        #     to_emails=to_emails,
        #     subject="Poročilo o stanju COVID pacientov v bolnišnicah na dan {}.".format(
        #         dateformat.format(datetime.datetime.utcnow().date(), "d-m-Y")
        #     ),
        #     html_content=html_content,
        # )
        # try:
        #     sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        #     response = sg.send(message)

        # except Exception as e:
        #     print(e.message)
        logger.info("EMAIL WOULD BE SENT NORMALLY.")

    # if not every active hospital reports is gathered,
    # but time for partial email send was already reached, send partial email
    else:
        logger.info(
            "Email ne bo poslan ker bolnišnice {} še niso poslale podatkov.".format(
                list_hospitals
            )
        )

