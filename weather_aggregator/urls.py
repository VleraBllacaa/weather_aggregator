from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bulgarian_meteo_pro/", include("bulgarian_meteo_pro.urls")),
    path("weather_master_x/", include("weather_master_x.urls")),
    path("stations/", include("stations.urls")),
]
