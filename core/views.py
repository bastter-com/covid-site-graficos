from django.shortcuts import render
from world.models import CountryData, WorldTotalData
from brazil.models import StateData


def index(request):
    total_data = WorldTotalData.objects.all().last()

    brazil_data = CountryData.objects.filter(country="Brazil").last()

    return render(
        request, "index.html", {"total_data": total_data, "brazil_data": brazil_data}
    )


def states(request):
    uf_list = (
        StateData.objects.values_list("state", flat=True).order_by("state").distinct()
    )

    return render(
        request, "brazil/states_list.html", {"context": uf_list, "navbar": "states"}
    )
