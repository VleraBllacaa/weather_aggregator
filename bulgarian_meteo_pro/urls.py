from django.urls import path
from . import views

urlpatterns = [
    path("weather-data/", views.create_weather_data, name="BMP_create_weather_data"),
    path(
        "weather-data/<str:city_name>/",
        views.get_weather_data_by_city,
        name="BMP_get_weather_data_by_city",
    ),
]
