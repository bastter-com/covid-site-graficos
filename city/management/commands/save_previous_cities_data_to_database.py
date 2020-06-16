from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from os import listdir
from city.models import CityData
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Save new Brazil states data to database"

    def handle(self, *args, **kwargs):
        path = f"{settings.BASE_DIR}/city/data/"
        csv_file = listdir(path)[0]
        if csv_file and csv_file.endswith('.csv'):
            with open(f"{path}{csv_file}", 'r') as file:
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
                        print(f"{date} - {city} - {state} - already in database")
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
                        print(f"{date} - {city} - {state} - saved to database!")

