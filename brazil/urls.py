from django.urls import path
from .views import brazil, state

urlpatterns = [
    path("", brazil, name="brazil"),
    path("<str:uf>", state, name="state"),
]
