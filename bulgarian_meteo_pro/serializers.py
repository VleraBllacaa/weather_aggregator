from rest_framework import serializers
from .models import BulgarianMeteoProData


class BulgarianMeteoProDataSerializer(serializers.ModelSerializer):
    station_id = serializers.CharField(source="station_identifier")
    city = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    temperature_celsius = serializers.FloatField()
    humidity_percent = serializers.FloatField()
    wind_speed_kph = serializers.FloatField()
    timestamp = serializers.DateTimeField(source="recorded_at")
    station_status = serializers.CharField(source="operational_status")

    class Meta:
        model = BulgarianMeteoProData
        fields = [
            "station_id",
            "city",
            "latitude",
            "longitude",
            "temperature_celsius",
            "humidity_percent",
            "wind_speed_kph",
            "timestamp",
            "station_status",
        ]
