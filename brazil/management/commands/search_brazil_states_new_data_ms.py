from django.core.management.base import BaseCommand
from brazil.services.update_data_using_ms_base import (
    pipeline_to_save_data_using_ms_source,
)
import datetime


class Command(BaseCommand):
    help = "Save new Brazil states data to database using Ministerio da Saude source"

    def add_arguments(self, parser):
        parser.add_argument(
            "--yesterday",
            help="Save yesterday's data when downloading the worksheet after the release date",
        )

    def handle(self, *args, **kwargs):
        yesterday_flag = kwargs["yesterday"]
        if yesterday_flag:
            date_today = datetime.date.today()
            yesterday = date_today - datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%Y-%m-%d")
            pipeline_to_save_data_using_ms_source(yesterday)
        else:
            pipeline_to_save_data_using_ms_source()
