from django.db import models


class WorldTotalData(models.Model):
    confirmed = models.IntegerField()
    recovered = models.IntegerField()
    deaths = models.IntegerField()
    active = models.IntegerField(blank=True)
    date = models.DateField(unique=True)


class CountryData(models.Model):
    country = models.CharField(max_length=60)
    translated_country_name = models.CharField(max_length=60)
    date = models.DateField()
    confirmed = models.IntegerField()
    recovered = models.IntegerField()
    deaths = models.IntegerField()
    active = models.IntegerField(blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.country} - {self.date}"
