import requests
from world.models import WorldTotalData
import datetime
from django.conf import settings


def create_date_list():
    if WorldTotalData.objects.all():
        now = datetime.date.today()
        base_date = datetime.date(2020, 1, 21)
        duration = now - base_date
        list_of_dates_to_check = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]
        last_date_in_database = WorldTotalData.objects.latest("date").date
        for index, date in enumerate(list_of_dates_to_check):
            if date == last_date_in_database:
                list_of_dates_to_save_data = list_of_dates_to_check[:index]
                break

    else:
        now = datetime.date.today()
        base_date = datetime.date(2020, 1, 21)
        duration = now - base_date
        list_of_dates_to_save_data = [
            now - datetime.timedelta(days=day) for day in range(duration.days)
        ]

    return [date.strftime("%Y-%m-%d") for date in list_of_dates_to_save_data]


def base_request(date):
    """
    Make request to get total values by date. If a new date is available,
    a call is made and if confirmed cases, a new row at WorldTotalData table
    is included.
    """
    url = "https://covid-19-data.p.rapidapi.com/report/totals"
    params = {
        "date-format": "undefined",
        "format": "undefined",
        "date": date,
    }
    headers = {
        "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
        "x-rapidapi-key": settings.X_RAPIDAPI_KEY,
    }
    request_data = requests.get(url, headers=headers, params=params)
    return request_data.json()[0]


def save_data_to_database(date, data):
    if WorldTotalData.objects.filter(date=date):
        print("This data is already at database")
        return False
    WorldTotalData.objects.create(
        confirmed=data["confirmed"],
        recovered=data["recovered"],
        deaths=data["deaths"],
        active=data["active"],
        date=data["date"],
    )
    print(f"Numbers of day {data['date']} saved at database!")


def search_for_empty_data_to_save_at_totals_data():
    date_list = create_date_list()
    date_list.reverse()
    for date in date_list:
        data = base_request(date)
        if data["confirmed"]:
            save_data_to_database(date, data)
