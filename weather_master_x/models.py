from django.db import models

from stations.models import BaseStation


# Create your models here.
class Coordinates(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()


class Location(models.Model):
    city_name = models.CharField(max_length=100)
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE)


class Readings(models.Model):
    temp_fahrenheit = models.FloatField()
    humidity_percent = models.FloatField()
    pressure_hpa = models.FloatField()
    uv_index = models.IntegerField()
    rain_mm = models.FloatField()


class WeatherMasterXData(BaseStation):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    readings = models.OneToOneField(Readings, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["city", "recorded_at"]),
        ]
        ordering = ["recorded_at"]  # Return data in chronological order
        abstract = False

    def __str__(self):
        return f"Station {self.station_identifier} - {self.location.city_name}"

    def save(self, *args, **kwargs):
        # Automatically populate city_name from the related Location model
        if self.location:
            self.city_name = self.location.city_name
        super().save(*args, **kwargs)
