from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
from brazil.models import StateData
from city.models import CityData


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

    queryset = CityData.objects.filter(state=uf, city=city).first()
    data = {
        "uf": queryset.state,
        "city": queryset.city,
        "confirmed": queryset.confirmed,
        "cases_rate_per_inhabitants": round(
            ((queryset.confirmed / queryset.estimated_population_2019) * 100),
            3,
        ),
        "deaths": queryset.deaths,
        "deaths_rate_per_inhabitants": round(
            ((queryset.deaths / queryset.estimated_population_2019) * 100), 3,
        ),
        "date": datetime.date.strftime(queryset.date, format="%d/%m/%Y"),
        "estimated_population_2019": queryset.estimated_population_2019,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
