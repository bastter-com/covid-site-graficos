from brazil.models import StateData


def get_state_detail(uf):
    queryset = StateData.objects.filter(state=uf.upper(), confirmed__gt=0).order_by(
        "date"
    )

    return queryset


def get_last_update_date(uf):
    last_update = StateData.objects.filter(state=uf.upper()).last().date

    return last_update


def get_state_name(uf):
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


def prepare_data_for_table(queryset):

    data_for_table = list()
    for daily_data in queryset:
        data_for_table.append(
            {
                "confirmed": daily_data.confirmed,
                "deaths": daily_data.deaths,
                "date": daily_data.date.strftime("%d/%m"),
                "confirmed_rate_by_100k_pop": round(
                    (
                        (daily_data.confirmed / daily_data.estimated_population_2019)
                        * 100000
                    ),
                    2,
                ),
                "deaths_rate_by_100k_pop": round(
                    (
                        (daily_data.deaths / daily_data.estimated_population_2019)
                        * 100000
                    ),
                    2,
                ),
            }
        )

    return data_for_table


def prepare_data_for_charts(queryset):
    confirmed = [data.confirmed for data in queryset]
    deaths = [data.deaths for data in queryset]
    new_confirmed = [
        day_after - day_before
        for day_before, day_after in zip(confirmed, confirmed[1:])
    ]
    new_confirmed.insert(0, confirmed[0])
    new_deaths = [
        day_after - day_before for day_before, day_after in zip(deaths, deaths[1:])
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
    queryset = get_state_detail(uf)
    last_update = get_last_update_date(uf)
    state_name = get_state_name(uf)
    data_for_table = prepare_data_for_table(queryset)
    data_for_charts = prepare_data_for_charts(queryset)

    return {
        "state_name": state_name,
        "state_uf": uf,
        "last_update": last_update,
        "data_for_table": data_for_table,
        "data_for_charts": data_for_charts,
    }
