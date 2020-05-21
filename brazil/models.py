from django.db import models


class StateData(models.Model):
    STATE_CHOICES = [
        ("SP", "SP"),
        ("AC", "AC"),
        ("AM", "AM"),
        ("RR", "RR"),
        ("PA", "PA"),
        ("AP", "AP"),
        ("TO", "TO"),
        ("MA", "MA"),
        ("PI", "PI"),
        ("CE", "CE"),
        ("RN", "RN"),
        ("PB", "PB"),
        ("PE", "PE"),
        ("AL", "AL"),
        ("SE", "SE"),
        ("BA", "BA"),
        ("MG", "MG"),
        ("ES", "ES"),
        ("RJ", "RJ"),
        ("RO", "RO"),
        ("PR", "PR"),
        ("SC", "SC"),
        ("RS", "RS"),
        ("MS", "MS"),
        ("MT", "MT"),
        ("GO", "GO"),
        ("DF", "DF"),
    ]

    state = models.CharField(max_length=30, choices=STATE_CHOICES)
    estimated_population_2019 = models.IntegerField()
    confirmed = models.IntegerField()
    date = models.DateField()
    deaths = models.IntegerField()

    class Meta:
        unique_together = ["state", "date"]

    def __str__(self):
        return f"{self.state} - {self.date}"
