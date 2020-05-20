from django.contrib import admin
from brazil.models import StateData


class StateDataAdmin(admin.ModelAdmin):
    list_display = ("state", "date", "confirmed", "deaths")


admin.site.register(StateData, StateDataAdmin)
