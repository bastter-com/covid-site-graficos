from django.urls import path
from .views import cities, cities_data, cities_detail


urlpatterns = [
    path("", cities, name="cities"),
    path("cidades_detalhe/", cities_detail, name="cidades_detalhe"),
    path("cidades_dados/", cities_data, name="cidades_dados"),
]
