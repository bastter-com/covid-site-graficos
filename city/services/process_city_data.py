from brazil.services.calculate_moving_average import calculate_moving_average


def prepare_data_for_charts(queryset):
    """
    Get and process data for state chats at detail endpoint.
    """
    confirmed = [data.confirmed for data in queryset]
    deaths = [data.deaths for data in queryset]
    new_confirmed = [
        day_after - day_before
        for day_before, day_after in zip(confirmed, confirmed[1:])
    ]
    new_confirmed.insert(0, confirmed[0])

    new_confirmed_moving_average = calculate_moving_average(new_confirmed, 7)

    new_deaths = [
        day_after - day_before
        for day_before, day_after in zip(deaths, deaths[1:])
    ]
    new_deaths.insert(0, deaths[0])

    new_deaths_moving_average = calculate_moving_average(new_deaths, 7)

    dates = [data.date.strftime("%d/%m") for data in queryset]
    confirmed_rate_by_100k_pop = [
        round(((data.confirmed / data.estimated_population_2019) * 100000), 2)
        for data in queryset
    ]
    deaths_rate_by_100k_pop = [
        round(((data.deaths / data.estimated_population_2019) * 100000), 2)
        for data in queryset
    ]
    data_for_charts = {
        "confirmed": confirmed,
        "deaths": deaths,
        "new_confirmed": new_confirmed,
        "new_confirmed_moving_average": new_confirmed_moving_average,
        "new_deaths": new_deaths,
        "new_deaths_moving_average": new_deaths_moving_average,
        "dates": dates,
        "confirmed_rate_by_100k_pop": confirmed_rate_by_100k_pop,
        "deaths_rate_by_100k_pop": deaths_rate_by_100k_pop,
    }

    return data_for_charts
