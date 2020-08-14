from django_docopt_command import DocOptCommand
from django.utils import timezone, dateformat
from HOS.models import ReportHOS, Report_type, Hospital, Email, Timeline
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

        # logger.info(render_to_string("HOS_email_template.html", {"context": context}))

        message = Mail(
            from_email="info@sledilnik.org",
            to_emails="matej@matejmeglic.com, donmatejo@gmail.com",
            subject="Poročilo o stanju COVID pacientov v bolnišnicah na dan {}.".format(
                dateformat.format(datetime.datetime.utcnow().date(), "d-m-Y")
            ),
            html_content=render_to_string(
                "HOS_email_template.html", {"context": context}
            ),
        )
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    else:
        logger.info(
            "email ne bo poslan ker {} še niso poslale podatkov.".format(list_hospitals)
        )

