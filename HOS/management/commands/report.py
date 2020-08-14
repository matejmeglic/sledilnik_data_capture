from django_docopt_command import DocOptCommand
from django.utils import timezone, dateformat
from HOS.models import ReportHOS, Hospital

import logging

logger = logging.getLogger("management.commands")


DOCS = """
Usage:
    report list [--count=<n>]
    report hos_report

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


def hos_report(count=None):
    queryset = ReportHOS.objects.all()
    queryset_hospitals = Hospital.objects.filter(is_active=True)
    today = dateformat.format(timezone.now(), "Y-m-d")

    list_hospitals = []
    for hospital in queryset_hospitals:
        list_hospitals.append(hospital.short_name)

    for report in queryset:
        if dateformat.format(report.date_reporting, "Y-m-d") == today:
            for hospital in queryset_hospitals:
                if report.hospital == hospital:
                    list_hospitals.remove(hospital.short_name)

    logger.info(list_hospitals)
    # logger.info(
    #     "{} - {} - {}".format(
    #         report.date_reporting,
    #         report.hospital.short_name,
    #         report.submitted_by,
    #     )
