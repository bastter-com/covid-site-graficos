from django.db import models


class StateData(models.Model):
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

    state = models.CharField(max_length=30, choices=STATE_CHOICES)
    update_source = models.CharField(
        max_length=30, choices=UPDATE_SOURCE_CHOICES
    )
    estimated_population_2019 = models.IntegerField()
    confirmed = models.IntegerField()
    date = models.DateField()
    deaths = models.IntegerField()

    class Meta:
        unique_together = ["state", "date"]

    def __str__(self):
        return f"{self.state} - {self.date}"
