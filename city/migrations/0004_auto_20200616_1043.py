# Generated by Django 3.0.7 on 2020-06-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("city", "0003_auto_20200524_0142"),
    ]

    operations = [
        migrations.AlterField(
            model_name="citydata",
            name="city_ibge_code",
            field=models.CharField(max_length=12),
        ),
        migrations.AlterUniqueTogether(
            name="citydata", unique_together={("city_ibge_code", "date")},
        ),
    ]
