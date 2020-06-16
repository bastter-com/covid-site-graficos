from city.models import CityData


def get_cities_data_of_an_uf(uf):
    """
    Get the cities data of a choosen UF.
    """
    last_date_of_updated_city_data = (
        CityData.objects.filter(state=uf).order_by("date").last().date
    )
    queryset = CityData.objects.filter(
        state=uf, date=last_date_of_updated_city_data
    )

    data = list(queryset.values())

    # Round decimal points of rates
    for city in data:
        city["confirmed_per_100k_inhabitants"] = round(
            city["confirmed_per_100k_inhabitants"], 2
        )
        city["death_per_100k_inhabitants"] = round(
            ((city["deaths"] / city["estimated_population_2019"]) * 100000), 2
        )

    return data
