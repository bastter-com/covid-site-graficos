from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from os import listdir, remove
from django.conf import settings
from time import sleep
from brazil.services.update_data_using_ms_base import (
    pipeline_to_download_xlsx_file,
    delete_xlsx_files_after_processing,
    open_xlsx_file_with_pandas,
    filter_dataframe_to_find_data_of_specific_date,
    cleanup_dataframe,
    iterate_dataframe_rows_and_save_new_data_in_database,
)
import csv
from brazil.models import StateData
from city.models import CityData


class UpdateDataUsingMSData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.xlsx_file = pipeline_to_download_xlsx_file()
        cls.df = open_xlsx_file_with_pandas(cls.xlsx_file)
        with open("brazil/data/brazil_statedata.csv") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                StateData.objects.create(
                    state=row[1],
                    estimated_population_2019=row[2],
                    confirmed=row[3],
                    date=row[4],
                    deaths=row[5],
                    update_source=row[6],
                )
        with open("city/data/city_citydata.csv") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                CityData.objects.create(
                    state=row[1],
                    city=row[2],
                    city_ibge_code=row[3],
                    confirmed=row[4],
                    confirmed_per_100k_inhabitants=row[5],
                    date=row[6],
                    death_rate=row[7],
                    deaths=row[8],
                    estimated_population_2019=row[9],
                    update_source=row[10],
                )

    @classmethod
    def tearDownClass(cls):
        [remove(file) for file in listdir(".") if file.endswith("xlsx")]

    def test_if_is_possible_to_download_the_xlsx_file(self):

        self.assertEqual("xlsx", self.xlsx_file.split(".")[-1])

    def test_if_dataframe_can_be_opened(self):

        self.assertIsInstance(self.df, pd.DataFrame)

    def test_if_dataframe_is_correctly_filtered(self):
        date = "2020-05-23"
        df = filter_dataframe_to_find_data_of_specific_date(self.df, date)

        self.assertEqual(date, df["data"].iloc[0])

    def test_if_dataframe_is_correctly_cleaned_to_query_database(self):

        df = cleanup_dataframe(self.df)

        self.assertIsInstance(df["codmun"].iloc[0], str)

    def test_saving_empty_instances_using_ms_data(self):
        df = filter_dataframe_to_find_data_of_specific_date(
            self.df, "2020-05-23"
        )

        save_data = iterate_dataframe_rows_and_save_new_data_in_database(df)
        self.assertTrue(save_data)

    def test_if_exists_any_xlsx_file_after_processing(self):
        delete_xlsx_files_after_processing()

        xlsx_files = [file for file in listdir(".") if file.endswith("xlsx")]

        self.assertFalse(xlsx_files)
