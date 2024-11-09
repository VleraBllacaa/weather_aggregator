from rest_framework import serializers
from .models import Coordinates, WeatherMasterXData, Location, Readings


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ["lat", "lon"]


class LocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()

    class Meta:
        model = Location
        fields = ["city_name", "coordinates"]


class ReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readings
        fields = [
            "temp_fahrenheit",
            "humidity_percent",
            "pressure_hpa",
            "uv_index",
            "rain_mm",
        ]


class WeatherMasterXDataSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    readings = ReadingsSerializer()

    class Meta:
        model = WeatherMasterXData
        fields = [
            "station_identifier",
            "location",
            "recorded_at",
            "readings",
            "operational_status",
            "created_at",
        ]

    def create(self, validated_data):
        # Extract nested data for location and readings
        location_data = validated_data.pop("location")
        coordinates_data = location_data.pop("coordinates")
        readings_data = validated_data.pop("readings")

        # Create the Coordinates, Location, and Readings instances
        coordinates = Coordinates.objects.create(**coordinates_data)
        location = Location.objects.create(coordinates=coordinates, **location_data)
        readings = Readings.objects.create(**readings_data)

        # Create the main WeatherMasterXData instance
        weather_data = WeatherMasterXData.objects.create(
            location=location,
            readings=readings,
            city=location.city_name,
            **validated_data
        )
        return weather_data
