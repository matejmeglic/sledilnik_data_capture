from django_docopt_command import DocOptCommand

from HOS.models import ReportHOS

import logging
logger = logging.getLogger('management.commands')


DOCS = '''
Usage:
    report list [--count=<n>]

Options:
    -h --help     Show this screen.
    --version     Show version.
'''


class Command(DocOptCommand):
    docs = DOCS

    def handle_docopt(self, args):
        if args['list']:
            list_reports(count=int(args['--count']))


def list_reports(count=None):
    queryset = ReportHOS.objects.all()
    if count:
        queryset = queryset[:count]
    for report in queryset:
        logger.info("{} - {} - {}".format(report.date_reporting, report.hospital.short_name, report.submitted_by))
