from django.db import models
from brazil.models import StateData


class CityData(models.Model):
    state = models.CharField(max_length=3)
    city = models.CharField(max_length=80)
    city_ibge_code = models.CharField(max_length=12)
    confirmed = models.PositiveIntegerField()
    confirmed_per_100k_inhabitants = models.FloatField()
    date = models.DateField()
    death_rate = models.FloatField()
    deaths = models.PositiveIntegerField()
    estimated_population_2019 = models.PositiveIntegerField()
