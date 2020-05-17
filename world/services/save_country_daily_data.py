import requests
from world.models import CountryData
import datetime
from django.conf import settings


def create_countries_names_list():
    """
    Create a list of countries translated names.
    """

    countries_translated = {
        # "USA": "Estados Unidos",
        # "Spain": "Espanha",
        # "Italy": "Itália",
        # "UK": "Reino Unido",
        # "France": "França",
        # "Germany": "Alemanha",
        # "Turkey": "Turquia",
        # "Russia": "Rússia",
        # "Iran": "Irã",
        # "China": "China",
        "Brazil": "Brasil",
        # "Canada": "Canadá",
        # "Belgium": "Bélgica",
        # "Netherlands": "Holanda",
        # "Peru": "Peru",
        # "India": "Índia",
        # "Switzerland": "Suíça",
        # "Portugal": "Portugal",
        # "Ecuador": "Equador",
        # "Saudi Arabia": "Arábia Saudita",
        # "Sweden": "Suécia",
        # "Ireland": "Irlanda",
        # "Mexico": "México",
        # "Pakistan": "Paquistão",
        # "Singapore": "Singapura",
        # "Chile": "Chile",
        # "Israel": "Israel",
        # "Austria": "Áustria",
        # "Japan": "Japão",
        # "Belarus": "Belarus",
        # "Qatar": "Catar",
        # "Poland": "Polônia",
        # "UAE": "Emirados Árabes Unidos",
        # "Romania": "Romênia",
        # "South Korea": "Coreia do Sul",
        # "Ukraine": "Ucrânia",
        # "Indonesia": "Indonésia",
        # "Denmark": "Dinamarca",
        # "Serbia": "Sérvia",
        # "Philippines": "Filipinas",
        # "Norway": "Noruega",
        # "Czech Republic": "República Tcheca",
        # "Bangladesh": "Bangladesh",
        # "Dominican Republic": "República Dominicana",
        # "Australia": "Austrália",
        # "Panama": "Panamá",
        # "Colombia": "Colômbia",
        # "Malaysia": "Malásia",
        # "South Africa": "África do Sul",
        # "Egypt": "Egito",
        # "Finland": "Finlândia",
        # "Argentina": "Argentina",
        # "Morocco": "Marrocos",
        # "Kuwait": "Kuwait",
        # "Algeria": "Algéria",
        # "Moldova": "Moldávia",
        # "Luxembourg": "Luxemburgo",
        # "Kazakhstan": "Cazaquistão",
        # "Bahrain": "Bahrein",
        # "Thailand": "Tailândia",
        # "Hungary": "Hungria",
        # "Greece": "Grécia",
        # "Oman": "Omã",
        # "Afghanistan": "Afeganistão",
        # "Iraq": "Iraque",
        # "Croatia": "Croácia",
        # "Ghana": "Gana",
        # "Armenia": "Armênia",
        # "Uzbekistan": "Uzbequistão",
        # "Nigeria": "Nigéria",
        # "Cameroon": "Camarões",
        # "Azerbaijan": "Azerbaijão",
        # "Iceland": "Islândia",
        # "Bosnia and Herzegovina": "Bósnia e Herzegovina",
        # "Estonia": "Estônia",
        # "Bulgaria": "Bulgária",
        # "Cuba": "Cuba",
        # "Guinea": "Guiné",
        # "New Zealand": "Nova Zelândia",
        # "North Macedonia": "Macedônia",
        # "Lithuania": "Lituânia",
        # "Slovenia": "Eslovênia",
        # "Slovakia": "Eslováquia",
        # "Ivory Coast": "Costa do Marfim",
        # "Bolivia": "Bolívia",
        # "Djibouti": "Djibouti",
        # "Hong Kong": "Hong Kong",
        # "Tunisia": "Tunísia",
        # "Senegal": "Senegal",
        # "Latvia": "Letônia",
        # "Cyprus": "Chipre",
        # "Albania": "Albânia",
        # "Honduras": "Honduras",
        # "Kyrgyzstan": "Quirguistão",
        # "Andorra": "Andorra",
        # "Lebanon": "Líbano",
        # "Costa Rica": "Costa Rica",
        # "Niger": "Níger",
        # "Sri Lanka": "Sri Lanka",
        # "Burkina Faso": "Burkina Faso",
        # "Uruguay": "Uruguai",
        # "Somalia": "Somália",
        # "Guatemala": "Guatemala",
        # "DRC": "República Democrática do Congo",
        # "San Marino": "San Marino",
        # "Georgia": "Geórgia",
        # "Mayotte": "Mayotte",
        # "Channel Islands": "Channel Islands",
        # "Mali": "Mali",
        # "Tanzania": "Tanzânia",
        # "Maldives": "Maldivas",
        # "Malta": "Malta",
        # "Jordan": "Jordânia",
        # "Sudan": "Sudão",
        # "Taiwan": "Taiwan",
        # "Jamaica": "Jamaica",
        # "Reunion": "Ilha da Reunião",
        # "Kenya": "Quênia",
        # "El Salvador": "El Salvador",
        # "Palestine": "Palestina",
        # "Venezuela": "Venezuela",
        # "Mauritius": "Ilhas Maurício",
        # "Montenegro": "Montenegro",
        # "Isle of Man": "Ilha de Man",
        # "Equatorial Guinea": "Guiné Equatorial",
        # "Gabon": "Gabão",
        # "Vietnam": "Vietnã",
        # "Paraguay": "Paraguai",
        # "Rwanda": "Ruanda",
        # "Congo": "Congo",
        # "Guinea-Bissau": "Guiné-Bissau",
        # "Faeroe Islands": "Ilhas Faróe",
        # "Martinique": "Martinica",
        # "Guadeloupe": "Guadalupe",
        # "Myanmar": "Myanmar",
    }

    return countries_translated


def create_date_list():
    """
    Create a base date list to search for empty data. 
    """
    if CountryData.objects.all():
        now = datetime.date.today()
        base_date = datetime.date(2020, 1, 21)
        duration = now - base_date
        list_of_dates_to_check = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]
        last_date_in_database = CountryData.objects.latest("date").date
        for index, date in enumerate(list_of_dates_to_check):
            if date == last_date_in_database:
                list_of_dates_to_save_data = list_of_dates_to_check[
                    : index + 2
                ]
                break
    else:
        now = datetime.date.today()
        base_date = datetime.date(2020, 1, 21)
        duration = now - base_date
        list_of_dates_to_save_data = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]
    return [date.strftime("%Y-%m-%d") for date in list_of_dates_to_save_data]


def base_request(date, country):
    """
    The base request to get countries data.
    """
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"
    params = {
        "date-format": "YYYY-MM-DD",
        "format": "json",
        "date": date,
        "name": country,
    }
    headers = {
        "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
        "x-rapidapi-key": settings.X_RAPIDAPI_KEY,
    }
    request_data = requests.get(url, headers=headers, params=params)
    return request_data.json()[0]


def save_data_to_database(date, data):
    """
    Save data in database of each country.
    """
    countries_list = create_countries_names_list()
    if CountryData.objects.filter(date=date, country=data["country"]):
        print("This data is already at database")
        return False
    CountryData.objects.create(
        country=data["country"],
        translated_country_name=countries_list[data["country"]],
        date=data["date"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        confirmed=sum(
            [province["confirmed"] for province in data["provinces"]]
        ),
        recovered=sum(
            [province["recovered"] for province in data["provinces"]]
        ),
        deaths=sum([province["deaths"] for province in data["provinces"]]),
        active=sum([province["active"] for province in data["provinces"]]),
    )
    print(f"Data of {data['country']} - {data['date']} saved at database!")


def search_for_empty_data_to_save_at_country_data():
    """
    Pipeline function to save data at cointry database table.
    """
    date_list = create_date_list()
    date_list.reverse()
    countries_list = create_countries_names_list()
    for date in date_list:
        for country in countries_list.keys():
            data = base_request(date, country)
            if "confirmed" in data["provinces"][0].keys():
                save_data_to_database(date, data)
