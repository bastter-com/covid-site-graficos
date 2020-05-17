from django.contrib import admin
from django.urls import path, include
import brazil.urls
import world.urls
from .views import index, states, cities, cities_detail, cities_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("brasil/", include(brazil.urls)),
    path("mundo/", include(world.urls)),
    path("estados/", states, name="states"),
    path("cidades/", cities, name="cities"),
    path("cidades_detalhe/", cities_detail, name="cidades_detalhe"),
    path("cidades_dados/", cities_data, name="cidades_dados"),
]
