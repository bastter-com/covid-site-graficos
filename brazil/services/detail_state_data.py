from brazil.models import StateData


def get_state_detail(uf):
    """
    Get data of a specific state.
    """
    queryset = StateData.objects.filter(
        state=uf.upper(), confirmed__gt=0
    ).order_by("date")

    return queryset


def get_last_update_date(uf):
    """
    Get the last updated data of one UF.
    """
    last_update = StateData.objects.filter(state=uf.upper()).last().date

    return last_update


def get_state_name(uf):
    """
    Get the state name using the UF name.
    """
    states_dict = {
        "AM": "Amazonas",
        "PA": "Pará",
        "AP": "Amapá",
        "RO": "Rondônia",
        "AC": "Acre",
        "RR": "Roraima",
        "TO": "Tocantins",
        "PE": "Pernambuco",
        "CE": "Ceará",
        "MA": "Maranhão",
        "BA": "Bahia",
        "AL": "Alagoas",
        "PB": "Paraíba",
        "RN": "Rio Grande do Norte",
        "PI": "Piauí",
        "SE": "Sergipe",
        "SP": "São Paulo",
        "RJ": "Rio de Janeiro",
        "ES": "Espírito Santo",
        "MG": "Minas Gerais",
        "DF": "Distrito Federal",
        "GO": "Goiás",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "SC": "Santa Catarina",
        "RS": "Rio Grande do Sul",
        "PR": "Paraná",
    }

    state = states_dict[uf]

    return state


def get_new_events_numbers(uf, data_to_query):
    """
    Get new cases or new deaths for state
    """
    queryset = StateData.objects.filter(state=uf.upper(), confirmed__gt=0).values_list(data_to_query, flat=True)
    data = list(queryset)
    new_events = [day_after - day_before for day_before, day_after in zip(data, data[1:])]
    new_events.insert(0, data[0])
    return new_events


def prepare_data_for_table(uf, queryset):
    """
    Get and process the data for table of detailed state data.
    """

    data_for_table = list()
    for daily_data in queryset:
        data_for_table.append(
            {
                "confirmed": daily_data.confirmed,
                "deaths": daily_data.deaths,
                "date": daily_data.date.strftime("%d/%m"),
                "confirmed_rate_by_100k_pop": round(
                    (
                        (
                            daily_data.confirmed
                            / daily_data.estimated_population_2019
                        )
                        * 100000
                    ),
                    2,
                ),
                "deaths_rate_by_100k_pop": round(
                    (
                        (
                            daily_data.deaths
                            / daily_data.estimated_population_2019
                        )
                        * 100000
                    ),
                    2,
                ),
            }
        )

    new_cases = get_new_events_numbers(uf, 'confirmed')
    new_deaths = get_new_events_numbers(uf, 'deaths')
    for index, day in enumerate(data_for_table):
        day['new_cases'] = new_cases[index]
        day['new_deaths'] = new_deaths[index]

    return data_for_table


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
    new_deaths = [
        day_after - day_before
        for day_before, day_after in zip(deaths, deaths[1:])
    ]
    new_deaths.insert(0, deaths[0])
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
        "new_deaths": new_deaths,
        "dates": dates,
        "confirmed_rate_by_100k_pop": confirmed_rate_by_100k_pop,
        "deaths_rate_by_100k_pop": deaths_rate_by_100k_pop,
    }

    return data_for_charts


def get_data_for_template(uf):
    """
    A pipeline function to get all data to send to templates.
    """
    queryset = get_state_detail(uf)
    last_update = get_last_update_date(uf)
    state_name = get_state_name(uf)
    data_for_table = prepare_data_for_table(uf, queryset)
    data_for_charts = prepare_data_for_charts(queryset)

    return {
        "state_name": state_name,
        "state_uf": uf,
        "last_update": last_update,
        "data_for_table": data_for_table,
        "data_for_charts": data_for_charts,
    }
