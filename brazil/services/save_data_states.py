import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ..models import StateData
import datetime
from time import sleep
from brazil.services.data_states_maps import create_base_date_list
from city.models import CityData
from time import sleep
from django.core.exceptions import ObjectDoesNotExist


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
            queryset = StateData.objects.filter(date=date, update_source="SES")

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
    if StateData.objects.filter(state=state, date=date, update_source="SES"):
        print("This data is already at database")
        return False
    elif StateData.objects.filter(state=state, date=date, update_source="MS"):

        data_to_update = StateData.objects.filter(
            state=state, date=date, update_source="MS"
        ).first()
        data_to_update.confirmed = data["confirmed"]
        data_to_update.deaths = data["deaths"]
        data_to_update.update_source = "SES"
        data_to_update.estimated_population_2019 = data[
            "estimated_population_2019"
        ]
        data_to_update.save()
        print(f"Data of {state} - {date} updated in database!")
        return True
    StateData.objects.create(
        state=state,
        estimated_population_2019=data["estimated_population_2019"],
        confirmed=data["confirmed"],
        deaths=data["deaths"],
        date=date,
        update_source="SES",
    )
    print(f"Data of {state} - {date} saved to database!")
    return True


def save_cities_data_to_database(state, data, date):
    """
    Save cities data to database if it is the last updated data.
    """
    # last_date_with_data = CityData.objects.filter(state=state, date=date).last()
    # if last_date_with_data:
    #     date = last_date_with_data.date
    # if date != last_date_with_data:
    for city in data:
        # state_to_database = StateData.objects.filter(state=state).last()
        # existing_city_or_not = CityData.objects.filter(
        #     city_ibge_code=city["city_ibge_code"]
        # )
        # if existing_city_or_not:
        #     existing_city_or_not.delete()
        flag_city_saved_or_not = False
        try:
            CityData.objects.get(city=city, date=date)
        except ObjectDoesNotExist:
            # from ipdb import set_trace; set_trace()
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
                    update_source="SES",
                )
            flag_city_saved_or_not = True
    if flag_city_saved_or_not:
        print(f"Cities of {state} - {date} saved to database!")
    else:
        print("There is no city data to save")


def save_previous_city_data_to_database():
    """
    Function to save previous data of each city.
    """
    now = datetime.date.today()
    base_date = datetime.date(2020, 2, 24)
    duration = now - base_date
    list_of_dates_to_check = [
        now - datetime.timedelta(days=day) for day in range(duration.days)
    ]
    list_of_dates_to_check.reverse()
    state_list = create_list_of_uf()

    for date in list_of_dates_to_check:
        for state in state_list:
            query = CityData.objects.filter(state=state, date=date).first()
            if not query:
                request = base_request(state, date)
                if request["results"]:
                    data = request["results"][:-1]
                    save_cities_data_to_database(state, data, date)


def fix_empty_registers_between_two_dates(
    uf, dates_list, index, date, queryset
):
    """
    Repeat previous data when existing register without data between
    two registers with data
    """
    for i in range(1, 10):
        if previous_data := StateData.objects.filter(
            date=dates_list[index - i], state=uf,
        ).first():
            queryset.state = uf
            queryset.estimated_population_2019 = (
                previous_data.estimated_population_2019
            )
            queryset.confirmed = previous_data.confirmed
            queryset.deaths = previous_data.deaths
            queryset.date = date
            queryset.save()


def save_empty_registers_before_first_register(uf, date):
    """
    Create registers without data but with date before first register
    """
    StateData.objects.create(
        state=uf,
        estimated_population_2019=0,
        confirmed=0,
        deaths=0,
        date=date,
    )


def copy_last_registers_and_save_between_two_dates(previous_data, uf, date):
    """
    Copy last data between two dates when a date haven't any data.
    """
    StateData.objects.create(
        state=uf,
        estimated_population_2019=(previous_data.estimated_population_2019),
        confirmed=previous_data.confirmed,
        deaths=previous_data.deaths,
        date=date,
    )


def update_registers_with_zero_confirmed_cases_between_two_dates(
    queryset, previous_data, uf, date
):
    """
    Update registers with no confirmed data existing between two dates.
    """
    queryset.state = uf
    queryset.estimated_population_2019 = (
        previous_data.estimated_population_2019
    )
    queryset.confirmed = previous_data.confirmed
    queryset.deaths = previous_data.deaths
    queryset.date = date
    queryset.save()


def search_for_empty_registers_between_two_dates_or_before_first_case():
    """
    Fix empty registers.
    Because the Brasil.IO API does not have data of all dates and all states,
    this function is needed to repeat the previous data when there is no data in
    some date or to add registers with zero cases before the first registered case.
    """
    dates_list_base_for_states_maps = create_base_date_list()[:-6]
    uf_list = create_list_of_uf()
    for index, date in enumerate(dates_list_base_for_states_maps):
        for uf in uf_list:
            queryset = StateData.objects.filter(date=date, state=uf).first()
            first_date_with_cases = (
                StateData.objects.filter(state=uf, confirmed__gt=0)
                .order_by("date")
                .first()
            ).date
            if date < first_date_with_cases:
                if not queryset:
                    save_empty_registers_before_first_register(uf, date)
            else:
                if not queryset:
                    for i in range(1, 10):
                        if previous_data := StateData.objects.filter(
                            date=dates_list_base_for_states_maps[index - i],
                            state=uf,
                        ).first():
                            copy_last_registers_and_save_between_two_dates(
                                previous_data, uf, date
                            )
                            break
                elif (
                    queryset.confirmed == 0
                    and queryset.date > first_date_with_cases
                ):
                    for i in range(1, 10):
                        if previous_data := StateData.objects.filter(
                            date=dates_list_base_for_states_maps[index - i],
                            state=uf,
                        ).first():
                            update_registers_with_zero_confirmed_cases_between_two_dates(
                                queryset, previous_data, uf, date
                            )

                            break


def search_for_empty_data_to_save():
    """
    Pipeline function to get non existing data and save at database.
    """
    date_list = create_date_list()
    date_list.reverse()
    state_list = create_list_of_uf()
    for date in date_list:
        for state in state_list:
            query = StateData.objects.filter(state=state, date=date).first()
            if query:
                query_update_source = query.update_source
            else:
                query_update_source = False
            if query_update_source == "MS" or not query:
                request = base_request(state, date)
                print(f"{date} - {state}")
                sleep(4)
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
                    queryset = CityData.objects.filter(
                            state=state, date=date
                        )
                    if not queryset:
                        data = request['results'][:-1]
                        save_cities_data_to_database(state, data, date)
                    # if request["results"][-1]["is_last"]:
                    #     queryset = CityData.objects.filter(
                    #         state=state, date=date
                    #     )
                    #     if not queryset:
                    #         data = request["results"][:-1]
                    #         save_cities_data_to_database(state, data, date)
                    #     else:
                    #         print(
                    #             f"Cities of {state} - {date} are already in database"
                    #         )

                else:
                    print("This state/date pair haven't data to save yet")
            else:
                print(f"{state} - {date} is already in database")
