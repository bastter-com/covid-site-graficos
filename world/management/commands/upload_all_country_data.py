from django.core.management.base import BaseCommand
import csv
from world.models import WorldTotalData
import os
from django.apps import apps
from datetime import datetime


class Command(BaseCommand):
    help = "Upload an existing csv file to WorldTotalData database"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = WorldTotalData

    def get_current_app_path(self):
        return apps.get_app_config("world").path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        file_path = os.path.join(app_path, "management", "commands", filename)
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
        with open(csv_file_path, "r") as file:
            has_header = csv.Sniffer().has_header(file.read())
            file.seek(0)
            reader = csv.reader(file, delimiter=",")
            if has_header:
                next(reader)
            for row in reader:
                confirmed = row[0]
                recovered = row[1]
                deaths = row[2]
                active = row[3]
                date = row[4].split("-")
                date = datetime(int(date[0]), int(date[1]), int(date[2]))
                WorldTotalData.objects.create(
                    confirmed=confirmed,
                    recovered=recovered,
                    deaths=deaths,
                    active=active,
                    date=date,
                )
            self.stdout.write(f"Data of {csv_file} succesfully uploaded to database")
