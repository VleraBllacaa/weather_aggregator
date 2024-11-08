from django.db import models

from stations.models import BaseStation


class BulgarianMeteoProData(BaseStation):
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percent = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed_kph = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["city", "recorded_at"]),
        ]
        ordering = ["recorded_at"]  # Return data in chronological order
        abstract = False

    def __str__(self):
        return f"""Station {self.station_identifier} in {self.city}
        recorded at {self.recorded_at}"""
