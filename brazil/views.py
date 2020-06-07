from django.shortcuts import render
from brazil.services import (
    data_states_maps,
    data_brazil_charts,
    detail_state_data,
    get_cities_data_for_detail_state_page,
)
from world.models import CountryData
from city.models import CityData
import json


def brazil(request):
    """
    View function for endpoint /brasil/
    """

    (
        daily_state_data,
        dates_list_base_for_states_map,
        region_cases,
        region_deaths,
        region_cases_100k_pop,
        region_deaths_100k_pop,
    ) = data_states_maps.get_data_for_each_state()

    total_data_brazil = data_brazil_charts.get_daily_data_for_brazil()

    last_update = CountryData.objects.filter(country="Brazil").last().date

    day_0_data, day_0_days = data_states_maps.get_data_day_zero_cases()

    list_of_ufs = list(data_states_maps.get_list_of_ufs())

    return render(
        request,
        "brazil/brazil.html",
        {
            "brazil_total_data": total_data_brazil,
            "states_daily_data": daily_state_data,
            "region_cases": region_cases,
            "region_deaths": region_deaths,
            "region_cases_100k_pop": region_cases_100k_pop,
            "region_deaths_100k_pop": region_deaths_100k_pop,
            "base_date_list_states_map": dates_list_base_for_states_map,
            "day_0_info": day_0_data,
            "day_0_days": day_0_days,
            "last_update": last_update,
            "list_of_ufs": list_of_ufs,
            "navbar": "brazil",
        },
    )


def state(request, uf):
    """
    View function for endpoint /<str:uf>/
    """

    total_data = detail_state_data.get_data_for_template(uf)

    cities_data = get_cities_data_for_detail_state_page.get_cities_data_of_an_uf(
        uf
    )

    last_date_with_cities_update = (
        CityData.objects.filter(state=uf.upper()).last().date
    )

    data_for_charts = total_data["data_for_charts"]

    # with open(f"static/json/{uf.upper()}.json") as json_file:
    #     map_geojson = json.load(json_file)

    return render(
        request,
        "brazil/state.html",
        {
            "uf": uf,
            "context": total_data,
            "data_for_charts": data_for_charts,
            "cities_data": cities_data,
            "last_date_with_cities_update": last_date_with_cities_update
            # "map_geojson": map_geojson,
        },
    )
