from django.core.management.base import BaseCommand
import csv
from django.conf import settings
import os
from city.models import CityData
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Save new Brazil states data to database"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = CityData

    def get_current_app_path(self):
        return apps.get_app_config("city").path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        file_path = os.path.join(app_path, "data", filename)
        return file_path

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Indicates the exactly csv file to upload to database",
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        csv_file_path = self.get_csv_file(csv_file)
        with open(csv_file_path, 'r') as file:
            has_header = csv.Sniffer().has_header(file.read())
            file.seek(0)
            reader = csv.reader(file, delimiter=',')
            if has_header:
                next(reader)
            for row in reader:
                state = row[1]
                city = row[2]
                city_ibge_code = row[3]
                confirmed = row[4]
                confirmed_per_100k_inhabitants = row[5]
                date = row[6]
                death_rate = row[7]
                deaths = row[8]
                estimated_population_2019 = row[9]
                update_source = row[10]
                
                try:
                    CityData.objects.get(state=state, date=date, city=city)
                    self.stdout.write(f"{date} - {city} - {state} - already in database")
                except ObjectDoesNotExist:
                    CityData.objects.create(
                        state=state,
                        city=city,
                        city_ibge_code=city_ibge_code,
                        confirmed=confirmed,
                        confirmed_per_100k_inhabitants=confirmed_per_100k_inhabitants,
                        date=date,
                        death_rate=death_rate,
                        deaths=deaths,
                        estimated_population_2019=estimated_population_2019,
                        update_source=update_source
                    )
                    self.stdout.write(f"{date} - {city} - {state} - saved to database!")

