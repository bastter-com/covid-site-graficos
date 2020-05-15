from django.core.management.base import BaseCommand
from brazil.services.save_data_states import search_for_empty_data_to_save


class Command(BaseCommand):
    help = "Save new Brazil states data to database"

    def handle(self, *args, **kwargs):
        search_for_empty_data_to_save()
