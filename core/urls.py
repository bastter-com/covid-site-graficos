from django.contrib import admin
from django.urls import path, include
import brazil.urls
import world.urls
from .views import index, states

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("brasil/", include(brazil.urls)),
    path("mundo/", include(world.urls)),
    path("estados/", states, name="states"),
]
