from django.urls import path, include
import brazil.urls
import world.urls
import city.urls
from .views import index, states

urlpatterns = [
    path("", index, name="index"),
    path("brasil/", include(brazil.urls)),
    path("mundo/", include(world.urls)),
    path("cidades/", include(city.urls)),
    path("estados/", states, name="states"),
]
