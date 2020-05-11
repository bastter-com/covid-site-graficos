from django.db import models


class StateData(models.Model):
    state = models.CharField(max_length=30)
    estimated_population_2019 = models.IntegerField()
    confirmed = models.IntegerField()
    date = models.DateField()
    deaths = models.IntegerField()

    class Meta:
        unique_together = ["state", "date"]

    def __str__(self):
        return f"{self.state} - {self.date}"
