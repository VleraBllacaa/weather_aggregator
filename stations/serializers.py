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
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    temperature = serializers.SerializerMethodField()

    def get_temperature(self, obj):
        temperature_type = self.context.get("temperature_type", "celsius").lower()

        # Check if the requested temperature type exists, otherwise perform conversion
        if temperature_type == "fahrenheit":
            if (
                hasattr(obj, "temperature_fahrenheit")
                and obj.temperature_fahrenheit is not None
            ):
                return obj.temperature_fahrenheit
            elif (
                hasattr(obj, "temperature_celsius")
                and obj.temperature_celsius is not None
            ):
                return round(obj.temperature_celsius * 9 / 5 + 32, 2)
        else:  # Default to Celsius
            if (
                hasattr(obj, "temperature_celsius")
                and obj.temperature_celsius is not None
            ):
                return obj.temperature_celsius
            elif (
                hasattr(obj, "temperature_fahrenheit")
                and obj.temperature_fahrenheit is not None
            ):
                return round((obj.temperature_fahrenheit - 32) * 5 / 9, 2)

        return None  # Return None if no temperature data is available

    def to_representation(self, instance):
        """
        Customize representation to populate fields based on instance type.
        """
        base_represantation = {}
        if isinstance(instance, BulgarianMeteoProData):
            base_represantation.update(
                {
                    "station_id": instance.station_identifier,
                    "city": instance.city,
                    "latitude": instance.latitude,
                    "longitude": instance.longitude,
                    "humidity_percent": instance.humidity_percent,
                    "wind_speed_kph": instance.wind_speed_kph,
                    "timestamp": instance.recorded_at,
                    "station_status": instance.operational_status,
                    "pressure_hpa": None,
                    "uv_index": None,
                    "rain_mm": None,
                    "temperature_celsius": instance.temperature_celsius,
                    "temperature_fahrenheit": round(
                        instance.temperature_celsius * 9 / 5 + 32, 2
                    ),
                    "created_at": instance.created_at,
                }
            )
        elif isinstance(instance, WeatherMasterXData):
            base_represantation.update(
                {
                    "station_id": instance.station_identifier,
                    "city": instance.city,
                    "latitude": instance.location.coordinates.lat,
                    "longitude": instance.location.coordinates.lon,
                    "humidity_percent": instance.readings.humidity_percent,
                    "wind_speed_kph": None,
                    "timestamp": instance.recorded_at,
                    "station_status": instance.operational_status,
                    "pressure_hpa": instance.readings.pressure_hpa,
                    "uv_index": instance.readings.uv_index,
                    "rain_mm": instance.readings.rain_mm,
                    "temperature_celsius": round(
                        (instance.readings.temp_fahrenheit - 32) * 5 / 9, 2
                    ),
                    "temperature_fahrenheit": instance.readings.temp_fahrenheit,
                    "created_at": instance.created_at,
                }
            )

        # Add the calculated `temperature` based on the requested type
        temperature_type = self.context.get("temperature_type", "celsius").lower()
        if temperature_type == "fahrenheit":
            if "temperature_fahrenheit" in base_represantation:
                base_represantation["temperature"] = base_represantation[
                    "temperature_fahrenheit"
                ]
            else:
                base_represantation["temperature"] = round(
                    (base_represantation["temperature_celsius"] * 9 / 5) + 32, 2
                )
            del base_represantation["temperature_celsius"]
            del base_represantation["temperature_fahrenheit"]
        if temperature_type == "celsius":
            if "temperature_celsius" in base_represantation:
                base_represantation["temperature"] = base_represantation[
                    "temperature_celsius"
                ]
            else:
                base_represantation["temperature"] = round(
                    (base_represantation["temperature_fahrenheit"] - 32) * 5 / 9, 2
                )
            del base_represantation["temperature_celsius"]
            del base_represantation["temperature_fahrenheit"]

        return base_represantation
