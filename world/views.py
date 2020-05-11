from django.shortcuts import render
from operator import itemgetter
from world.services import get_totals_data


def world(request):
    totals_data = get_totals_data.get_totals_data()
    return render(
        request, "world/world.html", {"totals_data": totals_data, "navbar": "world"},
    )
