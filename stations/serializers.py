from rest_framework import serializers
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from weather_master_x.models import WeatherMasterXData


class UnifiedWeatherDataSerializer(serializers.Serializer):
    station_id = serializers.CharField()
    city = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    temperature_celsius = serializers.FloatField()
    temperature_fahrenheit = serializers.FloatField()
    humidity_percent = serializers.FloatField()
    wind_speed_kph = serializers.FloatField(required=False, allow_null=True)
    pressure_hpa = serializers.FloatField(required=False, allow_null=True)
    uv_index = serializers.IntegerField(required=False, allow_null=True)
    rain_mm = serializers.FloatField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField()
    station_status = serializers.CharField(required=False, allow_null=True)
    operational_status = serializers.CharField(required=False, allow_null=True)

    def to_representation(self, instance):
        """
        Customize representation to populate fields based on instance type.
        """
        if isinstance(instance, BulgarianMeteoProData):
            return {
                "station_id": instance.station_identifier,
                "city": instance.city,
                "latitude": instance.latitude,
                "longitude": instance.longitude,
                "temperature_celsius": instance.temperature_celsius,
                "temperature_fahrenheit": instance.temperature_celsius * 9 / 5 + 32,
                "humidity_percent": instance.humidity_percent,
                "wind_speed_kph": instance.wind_speed_kph,
                "timestamp": instance.recorded_at,
                "station_status": instance.operational_status,
                # Fields not available in BulgarianMeteoPro will be None
                "pressure_hpa": None,
                "uv_index": None,
                "rain_mm": None,
            }
        elif isinstance(instance, WeatherMasterXData):
            return {
                "station_id": instance.station_identifier,
                "city": instance.location.city_name,
                "latitude": instance.location.coordinates.lat,
                "longitude": instance.location.coordinates.lon,
                "temperature_celsius": (instance.readings.temp_fahrenheit - 32) * 5 / 9,
                "temperature_fahrenheit": instance.readings.temp_fahrenheit,
                "humidity_percent": instance.readings.humidity_percent,
                "pressure_hpa": instance.readings.pressure_hpa,
                "uv_index": instance.readings.uv_index,
                "rain_mm": instance.readings.rain_mm,
                "timestamp": instance.recorded_at,
                "operational_status": instance.operational_status,
                # Fields not available in WeatherMasterX will be None
                "wind_speed_kph": None,
            }
        return super().to_representation(instance)
