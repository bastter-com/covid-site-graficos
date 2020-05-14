import requests
from django.conf import settings
import json


def create_ibge_states_code_dict():
    """
    Create a dict with states ibge codes to use in further functions.
    """
    ibge_states_code_dict = {
        "AM": 13,
        "PA": 15,
        "AP": 16,
        "RO": 11,
        "AC": 12,
        "RR": 14,
        "TO": 17,
        "PE": 26,
        "CE": 23,
        "MA": 21,
        "BA": 29,
        "AL": 27,
        "PB": 25,
        "RN": 24,
        "PI": 22,
        "SE": 28,
        "SP": 35,
        "RJ": 33,
        "ES": 32,
        "MG": 31,
        "DF": 53,
        "GO": 52,
        "MT": 51,
        "MS": 50,
        "SC": 42,
        "RS": 43,
        "PR": 41,
    }

    return ibge_states_code_dict


def base_request_geojson_data(uf):
    """
    The base request to get geojson states data by uf.
    """
    url = f"https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-{uf}-mun.json"

    data = requests.get(url)
    geojson = data.json()
    return geojson


def request_and_save_geojson_states():
    """
    Do the requests and save the states data.
    """
    path = f"{settings.BASE_DIR}/brazil/data/geojson/"
    states_ibge_codes = create_ibge_states_code_dict()
    for state, code in states_ibge_codes.items():
        geojson = base_request_geojson_data(code)
        correct_data = fix_wrong_encoded_names_of_states_json(state, geojson)
        with open(f"{path}{state}.json", "w", encoding="utf-8") as json_file:
            json.dump(correct_data, json_file, ensure_ascii=False)


def fix_wrong_encoded_names_of_states_json(uf, dict_of_cities_to_fix_name):
    """
    The downloaded json files above have wrong encoding in cities name.
    This function fix the cities names using IBGE API.
    """
    ibge_api_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    correct_data_name = requests.get(ibge_api_url)
    data_names_json = correct_data_name.json()
    for city in dict_of_cities_to_fix_name["features"]:
        for correct_city_name in data_names_json:

            if str(correct_city_name["id"]) == city["properties"]["id"]:
                city["properties"]["name"] = correct_city_name["nome"]
                city["properties"]["description"] = correct_city_name["nome"]

    return dict_of_cities_to_fix_name
