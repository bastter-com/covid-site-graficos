from django.core.management.base import BaseCommand
from world.services.save_total_world_data import (
    search_for_empty_data_to_save_at_totals_data,
)
from world.services.save_country_daily_data import (
    search_for_empty_data_to_save_at_country_data,
)


class Command(BaseCommand):
    help = "Save new world data to database"

    def handle(self, *args, **kwargs):
        search_for_empty_data_to_save_at_totals_data()
        search_for_empty_data_to_save_at_country_data()
