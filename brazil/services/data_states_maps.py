from brazil.models import StateData
from operator import itemgetter
import datetime


def create_base_date_list():
    """
    Create a base date list to search on API for new data to put on database.
    """
    first_date_for_date_list = datetime.date(2020, 2, 24)
    now = StateData.objects.all().order_by("date").last().date
    duration = now - first_date_for_date_list
    dates_list_base_for_states_map = [
        (now - datetime.timedelta(days=day)) for day in range(duration.days)
    ]
    dates_list_base_for_states_map.reverse()
    return dates_list_base_for_states_map


def create_region_dict():
    """
    Create a base brazilian regions dict for regions charts for brazil endpoint.
    """
    return {
        "Norte": 0,
        "Nordeste": 0,
        "Sudeste": 0,
        "Centro-Oeste": 0,
        "Sul": 0,
    }


def get_data_for_each_state():
    """
    Get each state data making queries at database to plot on front-end brazil endpoint.
    """
    state_data_query = StateData.objects.all().order_by("date")
    states_data = [data for data in state_data_query]
    uf_query = StateData.objects.values_list("state", flat=True).distinct()
    uf_list = [uf for uf in uf_query]
    daily_state_data = list()
    for uf in uf_list:
        data = [info for info in states_data if info.state == uf]
        confirmed_by_state = list()
        deaths_by_state = list()
        dates_by_state = list()

        for state in data:
            confirmed_by_state.append(state.confirmed)
            deaths_by_state.append(state.deaths)
            dates_by_state.append(state.date.strftime("%d/%m"))
        new_confirmed_by_state = [
            day_after - day_before
            for day_before, day_after in zip(
                confirmed_by_state, confirmed_by_state[1:]
            )
        ]
        new_confirmed_by_state.insert(0, confirmed_by_state[0])
        new_deaths_by_state = [
            day_after - day_before
            for day_before, day_after in zip(
                deaths_by_state, deaths_by_state[1:]
            )
        ]
        new_deaths_by_state.insert(0, deaths_by_state[0])
        daily_state_data.append(
            {
                "state": uf,
                "confirmed": confirmed_by_state,
                "new_confirmed": new_confirmed_by_state,
                "deaths": deaths_by_state,
                "new_deaths": new_deaths_by_state,
                "dates": dates_by_state,
                "first_case_date": dates_by_state[
                    [
                        (index, cases)
                        for index, cases in enumerate(confirmed_by_state)
                        if cases >= 1
                    ][0][0]
                ],
                "last_date_with_updated_data": dates_by_state[-1],
                "total_cases": confirmed_by_state[-1],
                "total_deaths": deaths_by_state[-1],
                "lethality": round(
                    ((deaths_by_state[-1] / confirmed_by_state[-1]) * 100), 2
                ),
                "estimated_population_2019": state.estimated_population_2019,
                "cases_per_100k_pop": round(
                    (
                        (
                            confirmed_by_state[-1]
                            / state.estimated_population_2019
                        )
                        * 100000
                    ),
                    2,
                ),
                "deaths_per_100k_pop": round(
                    (
                        (deaths_by_state[-1] / state.estimated_population_2019)
                        * 100000
                    ),
                    2,
                ),
                "cases_rate_per_100k_pop": [
                    round(
                        (
                            (confirmed / state.estimated_population_2019)
                            * 100000
                        ),
                        2,
                    )
                    for confirmed in confirmed_by_state
                ],
                "deaths_rate_per_100k_pop": [
                    round(
                        ((deaths / state.estimated_population_2019) * 100000),
                        2,
                    )
                    for deaths in deaths_by_state
                ],
            }
        )
    daily_state_data = sorted(
        daily_state_data, key=itemgetter("total_cases"), reverse=True
    )

    dates_list_base_for_states_map = create_base_date_list()
    dates_list_base_for_states_map = [
        date.strftime("%d/%m") for date in dates_list_base_for_states_map
    ]

    region_confirmed = create_region_dict()

    region_deaths = create_region_dict()

    region_confirmed_100k_pop_rate = create_region_dict()

    region_deaths_100k_pop_rate = create_region_dict()

    state_and_region = {
        "AM": "Norte",
        "PA": "Norte",
        "AP": "Norte",
        "RO": "Norte",
        "AC": "Norte",
        "RR": "Norte",
        "TO": "Norte",
        "PE": "Nordeste",
        "CE": "Nordeste",
        "MA": "Nordeste",
        "BA": "Nordeste",
        "AL": "Nordeste",
        "PB": "Nordeste",
        "RN": "Nordeste",
        "PI": "Nordeste",
        "SE": "Nordeste",
        "SP": "Sudeste",
        "RJ": "Sudeste",
        "ES": "Sudeste",
        "MG": "Sudeste",
        "DF": "Centro-Oeste",
        "GO": "Centro-Oeste",
        "MT": "Centro-Oeste",
        "MS": "Centro-Oeste",
        "SC": "Sul",
        "RS": "Sul",
        "PR": "Sul",
    }

    for state in daily_state_data:

        uf = state["state"]
        region = state_and_region[uf]
        region_confirmed[region] += state["confirmed"][-1]
        region_deaths[region] += state["deaths"][-1]
        region_confirmed_100k_pop_rate[region] += state[
            "cases_rate_per_100k_pop"
        ][-1]
        region_deaths_100k_pop_rate[region] += state[
            "deaths_rate_per_100k_pop"
        ][-1]

    return (
        daily_state_data,
        dates_list_base_for_states_map,
        region_confirmed,
        region_deaths,
        region_confirmed_100k_pop_rate,
        region_deaths_100k_pop_rate,
    )


def get_data_day_zero_cases():
    """
    Get data only of states with more than 1000 cases of Covid-19.
    This data will be plot on front-end application on charts
    'number of events after case number 1000'.
    """
    length_of_days = len(
        StateData.objects.filter(confirmed__gte=1000, state="SP")
    )
    x_axis_days = [day for day in range(1, length_of_days + 1)]
    queryset = StateData.objects.filter(confirmed__gte=1000).order_by(
        "date", "confirmed"
    )
    data_list = [data for data in queryset]
    uf_query = (
        StateData.objects.filter(confirmed__gt=1000)
        .values_list("state", flat=True)
        .distinct()
    )
    data_day_0 = list()
    for uf in uf_query:
        data = [info for info in data_list if info.state == uf]
        confirmed_day_0 = list()
        deaths_day_0 = list()
        for state in data:
            confirmed_day_0.append(state.confirmed)
            deaths_day_0.append(state.deaths)
        data_day_0.append(
            {
                "state": uf,
                "confirmed_day_0": confirmed_day_0,
                "deaths_day_0": deaths_day_0,
                "confirmed_rate_by_100k_pop": [
                    round(
                        (
                            (confirmed / state.estimated_population_2019)
                            * 100000
                        ),
                        2,
                    )
                    for confirmed in confirmed_day_0
                ],
                "deaths_rate_by_100k_pop": [
                    round(
                        ((deaths / state.estimated_population_2019) * 100000),
                        2,
                    )
                    for deaths in deaths_day_0
                ],
                "total_cases": confirmed_day_0[-1],
                "total_deaths": deaths_day_0[-1],
            }
        )
    data_day_0 = sorted(
        data_day_0, key=itemgetter("total_cases"), reverse=True
    )

    return (data_day_0, x_axis_days)
