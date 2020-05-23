from world.models import CountryData
from brazil.services.calculate_moving_average import calculate_moving_average


def get_daily_data_for_brazil():
    """
    Get info to brazilian data to plot the first charts of brazil endpoint.
    """
    brazil_queryset = CountryData.objects.filter(
        country="Brazil", confirmed__gt=0
    ).order_by("date")

    confirmed_brazil = [data.confirmed for data in brazil_queryset]

    new_confirmed = [
        day_after - day_before
        for day_before, day_after in zip(
            confirmed_brazil, confirmed_brazil[1:]
        )
    ]
    new_confirmed.insert(0, confirmed_brazil[0])

    new_confirmed_moving_average_of_a_week = calculate_moving_average(
        new_confirmed, 7
    )

    recovered_brazil = [data.recovered for data in brazil_queryset]
    new_recovered = [
        day_after - day_before
        for day_before, day_after in zip(
            recovered_brazil, recovered_brazil[1:]
        )
    ]
    new_recovered.insert(0, recovered_brazil[0])

    new_recovered_moving_average_of_a_week = calculate_moving_average(
        new_recovered, 7
    )

    deaths_brazil = [data.deaths for data in brazil_queryset]
    new_deaths = [
        day_after - day_before
        for day_before, day_after in zip(deaths_brazil, deaths_brazil[1:])
    ]
    new_deaths.insert(0, deaths_brazil[0])

    new_deaths_moving_average_of_a_week = calculate_moving_average(
        new_deaths, 7
    )

    dates_list = [data.date.strftime("%d/%m") for data in brazil_queryset]

    return {
        "data": {
            "confirmed_brazil": confirmed_brazil,
            "new_confirmed": new_confirmed,
            "new_confirmed_moving_average": new_confirmed_moving_average_of_a_week,
            "recovered_brazil": recovered_brazil,
            "new_recovered": new_recovered,
            "new_recovered_moving_average": new_recovered_moving_average_of_a_week,
            "deaths_brazil": deaths_brazil,
            "new_deaths": new_deaths,
            "new_deaths_moving_average": new_deaths_moving_average_of_a_week,
            "dates_brazil": dates_list,
        }
    }
