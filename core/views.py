from django.shortcuts import render
from django.http import HttpResponse
import json
from world.models import CountryData, WorldTotalData
from brazil.models import StateData
from city.models import CityData
import datetime


def index(request):
    total_data = WorldTotalData.objects.all().last()

    brazil_data = CountryData.objects.filter(country="Brazil").last()

    return render(
        request,
        "index.html",
        {"total_data": total_data, "brazil_data": brazil_data},
    )


def states(request):
    uf_list = (
        StateData.objects.values_list("state", flat=True)
        .order_by("state")
        .distinct()
    )

    return render(
        request,
        "brazil/states_list.html",
        {"context": uf_list, "navbar": "states"},
    )


def cities(request):
    states_uf = (
        StateData.objects.all().values_list("state", flat=True).distinct()
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
    cities_of_selected_uf = CityData.objects.filter(
        state=uf.upper()
    ).values_list("city", flat=True)
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
        "deaths": queryset.deaths,
        "date": datetime.date.strftime(queryset.date, format="%d/%m/%Y"),
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
