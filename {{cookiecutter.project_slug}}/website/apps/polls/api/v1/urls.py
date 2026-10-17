from django.urls import path

from .views import PollListCreateAPI

app_name = "v1"

urlpatterns = [
    path("polls/", PollListCreateAPI.as_view(), name="polls"),
]
