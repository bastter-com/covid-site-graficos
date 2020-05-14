import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ..models import StateData
import datetime
from time import sleep
from brazil.services.data_states_maps import create_base_date_list
from city.models import CityData


def create_list_of_uf():
    """
    Define a list with all Brazil UF names
    """

    uf_list = [
        "SP",
        "AC",
        "AM",
        "RR",
        "PA",
        "AP",
        "TO",
        "MA",
        "PI",
        "CE",
        "RN",
        "PB",
        "PE",
        "AL",
        "SE",
        "BA",
        "MG",
        "ES",
        "RJ",
        "RO",
        "PR",
        "SC",
        "RS",
        "MS",
        "MT",
        "GO",
        "DF",
    ]

    return uf_list


def create_date_list():
    """
    Get a list of dates to include data on database.
    """

    if StateData.objects.all():
        now = datetime.date.today()
        base_date = datetime.date(2020, 2, 24)
        duration = now - base_date
        list_of_dates_to_check = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]
        for index, date in enumerate(list_of_dates_to_check):
            queryset = StateData.objects.filter(date=date)
            if len(queryset) == 27 and index != 0:
                if index != 0:
                    first_date = list_of_dates_to_check[index - 1]
                    index = list_of_dates_to_check.index(first_date)
                    first_date = first_date.strftime("%Y-%m-%d")
                    list_of_dates_to_save_data = list_of_dates_to_check[
                        : index + 1
                    ]
                    break
                else:
                    first_date = list_of_dates_to_check[0].strftime("%Y-%m-%d")
                    list_of_dates_to_save_data = [first_date]
    else:
        now = datetime.date.today()
        base_date = datetime.date(2020, 2, 24)
        duration = now - base_date
        list_of_dates_to_save_data = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]

    return [date.strftime("%Y-%m-%d") for date in list_of_dates_to_save_data]


def base_request(state, date):
    """
    A base request to get data by state and date.
    """
    session = requests.Session()
    retry = Retry(connect=4, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    url = f"https://brasil.io/api/dataset/covid19/caso/data/?state={state}&date={date}"
    request = session.get(url)
    data = request.json()
    return data


def save_data_to_database(state, data, date):
    """
    Save data to database if it doesn't exist yet.
    """
    if StateData.objects.filter(state=state, date=date):
        print("This data is already at database")
        return False
    StateData.objects.create(
        state=state,
        estimated_population_2019=data["estimated_population_2019"],
        confirmed=data["confirmed"],
        deaths=data["deaths"],
        date=date,
    )
    print(f"Data of {state} - {date} saved at database!")
    return True


def save_cities_data_to_database(state, data, date):
    """
    Save cities data to database if it is the last updated data.
    """
    last_date_with_data = CityData.objects.filter(date=date).last()
    if last_date_with_data:
        date = last_date_with_data.date
    if date != last_date_with_data:
        for city in data:
            state_to_database = StateData.objects.filter(state=state).last()
            existing_city_or_not = CityData.objects.filter(
                city_ibge_code=city["city_ibge_code"]
            )
            if existing_city_or_not:
                existing_city_or_not.delete()
            print(city["city"])
            if city["city_ibge_code"] and city["confirmed"]:
                CityData.objects.create(
                    state=city["state"],
                    city=city["city"],
                    city_ibge_code=city["city_ibge_code"],
                    confirmed=city["confirmed"],
                    confirmed_per_100k_inhabitants=city[
                        "confirmed_per_100k_inhabitants"
                    ],
                    date=city["date"],
                    death_rate=city["death_rate"],
                    deaths=city["deaths"],
                    estimated_population_2019=city[
                        "estimated_population_2019"
                    ],
                )
                print(f"Data of {date} -> {state} - {city} saved at database!")
        return True
    return False


def fix_empty_date_registers():
    """
    Create first registers of each state when they don't have data yet.
    """
    dates_list_base_for_states_maps = create_base_date_list()[:-5]
    uf_list = create_list_of_uf()
    for date in dates_list_base_for_states_maps:
        for uf in uf_list:
            queryset = StateData.objects.filter(date=date, state=uf)
            if not queryset:
                StateData.objects.create(
                    state=uf,
                    estimated_population_2019=0,
                    confirmed=0,
                    deaths=0,
                    date=date,
                )


def search_for_empty_data_to_save():
    """
    Pipeline function to get non existing data and save at database.
    """
    date_list = create_date_list()
    date_list.reverse()
    state_list = create_list_of_uf()
    for date in date_list:
        for state in state_list:
            request = base_request(state, date)
            print(f"{date} - {state}")
            sleep(5)
            if request["results"]:
                state_data = request["results"][-1]
                if state_data["place_type"] == "state":
                    data = {
                        "confirmed": state_data["confirmed"],
                        "deaths": state_data["deaths"],
                        "estimated_population_2019": state_data[
                            "estimated_population_2019"
                        ],
                    }
                    save_data_to_database(state, data, date)
                if request["results"][-1]["is_last"]:
                    data = request["results"][:-1]
                    save_cities_data_to_database(state, data, date)

            else:
                print("This state/date pair haven't data to save yet")
