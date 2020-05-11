from django.test import TestCase
import requests


class BaseTestCase(TestCase):
    def setUp(self):
        self.url_for_table = "https://api.covid19.finspect.me/brcovid19/map"
        self.url_for_daily_data = "https://api.covid19.finspect.me/brcovid19/map"
        self.base_url_for_detailed_cases_deaths_etc_info = "https://brasil.io/api/dataset/covid19/caso/data/"


class RequestsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_if_request_map_url_return_200(self):
        response_200_ok = requests.get(self.url_for_table)
        self.assertEqual(response_200_ok.status_code, 200)

    def test_if_request_daily_info_url_return_200(self):
        response_200_ok = requests.get(self.url_for_daily_data)
        self.assertEqual(response_200_ok.status_code, 200)

    def test_if_request_map_url_return_27_states_data(self):
        request = requests.get(self.url_for_table).json()
        self.assertEqual(len(request), 27)

    def test_if_request_detailed_cases_return_200(self):
        endpoint = "?state=SP&date=2020-03-30"
        request = requests.get(self.base_url_for_detailed_cases_deaths_etc_info + endpoint)
        self.assertEqual(request.status_code, 200)

    