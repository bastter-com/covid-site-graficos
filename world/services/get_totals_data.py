from world.models import WorldTotalData


def get_totals_data():
    """
    Get all data to send to endpoint of world data.
    """
    queryset = WorldTotalData.objects.all().order_by("date")
    total_confirmed = [data.confirmed for data in queryset]
    new_confirmed = [
        day_after - day_before
        for day_before, day_after in zip(total_confirmed, total_confirmed[1:])
    ]
    new_confirmed.insert(0, new_confirmed[0])
    total_deaths = [data.deaths for data in queryset]
    new_deaths = [
        day_after - day_before
        for day_before, day_after in zip(total_deaths, total_deaths[1:])
    ]
    new_deaths.insert(0, new_deaths[0])
    total_recovered = [data.recovered for data in queryset]
    new_recovered = [
        day_after - day_before
        for day_before, day_after in zip(total_recovered, total_recovered[1:])
    ]
    new_recovered.insert(0, total_recovered[1:])
    dates = [data.date.strftime("%d/%m") for data in queryset]

    return {
        "data": {
            "confirmed": total_confirmed,
            "new_confirmed": new_confirmed,
            "deaths": total_deaths,
            "new_deaths": new_deaths,
            "recovered": total_recovered,
            "new_recovered": new_recovered,
            "dates": dates,
        }
    }
