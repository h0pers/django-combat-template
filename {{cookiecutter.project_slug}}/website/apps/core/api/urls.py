from django.urls import path

from apps.core.api.views import health, health_ready

app_name = "core"

urlpatterns = [
    path("health/", health, name="health"),
    path("health/ready/", health_ready, name="health-ready"),
]
