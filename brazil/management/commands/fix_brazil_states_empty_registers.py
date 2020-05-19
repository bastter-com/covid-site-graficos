from django.core.management.base import BaseCommand
from brazil.services.save_data_states import (
    search_for_empty_registers_between_two_dates_or_before_first_case,
)


class Command(BaseCommand):
    help = "Save new Brazil states data to database"

    def handle(self, *args, **kwargs):
        search_for_empty_registers_between_two_dates_or_before_first_case()
