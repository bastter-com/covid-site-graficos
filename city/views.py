from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
from brazil.models import StateData
from city.models import CityData
from city.services import process_city_data


def cities(request):
    states_uf = (
        StateData.objects.all()
        .order_by("state")
        .values_list("state", flat=True)
        .distinct()
    )

    states = list()
    for uf in states_uf:
        states.append({"UF": uf})

    return render(
        request,
        "brazil/cities.html",
        {"navbar": "cities", "states_uf": states,},
    )


def cities_detail(request):

    uf = request.GET["uf"]
    cities_of_selected_uf = (
        CityData.objects.filter(state=uf.upper())
        .distinct("city")
        .order_by("city")
        .values_list("city", flat=True)
    )
    cities = list()
    for city in cities_of_selected_uf:
        cities.append({"name": city})
    return HttpResponse(json.dumps(cities), content_type="application/json",)


def cities_data(request):

    uf = request.GET["uf"]
    city = request.GET["city"]

    queryset = CityData.objects.filter(state=uf, city=city).order_by("date")
    city_data_for_charts = process_city_data.prepare_data_for_charts(queryset)
    queryset_for_card = (
        CityData.objects.filter(state=uf, city=city).order_by("date").last()
    )
    city_data_for_card = {
        "uf": queryset_for_card.state,
        "city": queryset_for_card.city,
        "confirmed": queryset_for_card.confirmed,
        "cases_rate_per_inhabitants": round(
            (
                (
                    queryset_for_card.confirmed
                    / queryset_for_card.estimated_population_2019
                )
                * 100
            ),
            3,
        ),
        "deaths": queryset_for_card.deaths,
        "deaths_rate_per_inhabitants": round(
            (
                (
                    queryset_for_card.deaths
                    / queryset_for_card.estimated_population_2019
                )
                * 100
            ),
            3,
        ),
        "date": datetime.date.strftime(
            queryset_for_card.date, format="%d/%m/%Y"
        ),
        "estimated_population_2019": queryset_for_card.estimated_population_2019,
    }
    city_data = [city_data_for_charts, city_data_for_card]
    return HttpResponse(json.dumps(city_data), content_type="application/json")
