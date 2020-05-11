from django.urls import path
from .views import world


urlpatterns = [path("", world, name="world")]
