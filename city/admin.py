from django.contrib import admin
from city.models import CityData


class CityDataAdmin(admin.ModelAdmin):
    list_display = ("state", "city", "confirmed", "date", "deaths")


admin.site.register(CityData, CityDataAdmin)
