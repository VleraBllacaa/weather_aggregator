from django.urls import path
from . import views

urlpatterns = [
    path(
        "weather-data/<str:city_name>/",
        views.get_weather_data_by_city,
        name="ST_get_weather_data_by_city",
    ),
    path(
        "weather-data/historical/<str:city_name>",
        views.get_historical_data,
        name="ST_get_historical_data",
    ),
]
