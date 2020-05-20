from django.contrib import admin
from world.models import WorldTotalData, CountryData


class WorldTotalDataAdmin(models.ModelAdmin):
    list_display = ("confirmed", "recovered", "deaths", "active", "date")


class CountryDataAdmin(models.ModelAdmin):
    list_display = (
        "country",
        "date",
        "confirmed",
        "recovered",
        "deaths",
        "active",
    )


admin.site.register(WorldTotalData, WorldTotalDataAdmin)
admin.site.register(CountryData, CountryDataAdmin)
