from django.db import models
from brazil.models import StateData


class CityData(models.Model):
    STATE_CHOICES = [
        ("AC", "AC"),
        ("AL", "AL"),
        ("AM", "AM"),
        ("AP", "AP"),
        ("BA", "BA"),
        ("CE", "CE"),
        ("DF", "DF"),
        ("ES", "ES"),
        ("GO", "GO"),
        ("MA", "MA"),
        ("MG", "MG"),
        ("MS", "MS"),
        ("MT", "MT"),
        ("PA", "PA"),
        ("PB", "PB"),
        ("PE", "PE"),
        ("PI", "PI"),
        ("PR", "PR"),
        ("RJ", "RJ"),
        ("RN", "RN"),
        ("RO", "RO"),
        ("RR", "RR"),
        ("RS", "RS"),
        ("SC", "SC"),
        ("SE", "SE"),
        ("SP", "SP"),
        ("TO", "TO"),
    ]

    UPDATE_SOURCE_CHOICES = [
        ("MS", "Ministério da Saúde"),
        ("SES", "Secretaria Estadual de Saúde"),
    ]
    state = models.CharField(max_length=3, choices=STATE_CHOICES)
    update_source = models.CharField(
        max_length=30, choices=UPDATE_SOURCE_CHOICES
    )
    city = models.CharField(max_length=80)
    city_ibge_code = models.CharField(max_length=12)
    confirmed = models.PositiveIntegerField()
    confirmed_per_100k_inhabitants = models.FloatField()
    date = models.DateField()
    death_rate = models.FloatField()
    deaths = models.PositiveIntegerField()
    estimated_population_2019 = models.PositiveIntegerField()

    class Meta:
        unique_together = ["city_ibge_code", "date"]

    def __str__(self):
        return f"{self.state} - {self.city} - {self.date}"
