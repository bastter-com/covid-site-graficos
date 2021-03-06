# Generated by Django 3.0.5 on 2020-05-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CityData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.CharField(max_length=3)),
                ("city", models.CharField(max_length=80)),
                ("city_ibge_code", models.CharField(max_length=12)),
                ("confirmed", models.PositiveIntegerField()),
                ("confirmed_per_100k_inhabitants", models.FloatField()),
                ("date", models.DateField()),
                ("death_rate", models.FloatField()),
                ("deaths", models.PositiveIntegerField()),
                ("estimated_population_2019", models.PositiveIntegerField()),
            ],
        ),
    ]
