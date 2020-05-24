from django.core.management.base import BaseCommand
from brazil.services.update_data_using_ms_base import (
    pipeline_to_save_data_using_ms_source,
)


class Command(BaseCommand):
    help = "Save new Brazil states data to database using Ministerio da Saude source"

    def handle(self, *args, **kwargs):
        pipeline_to_save_data_using_ms_source()
