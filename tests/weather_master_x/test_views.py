from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from weather_master_x.models import WeatherMasterXData, Location, Coordinates, Readings
from weather_master_x.serializers import WeatherMasterXDataSerializer


class WeatherMasterXDataTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse("WMX_create_weather_data")
        self.get_url = reverse("WMX_get_weather_data_by_city", args=["Sample City"])
        self.data = {
            "station_identifier": "ST123",
            "location": {
                "city_name": "Sample City",
                "coordinates": {"lat": 45.0, "lon": -93.0},
            },
            "recorded_at": "2024-11-08T12:00:00Z",
            "readings": {
                "temp_fahrenheit": 75.5,
                "humidity_percent": 60.0,
                "pressure_hpa": 1013,
                "uv_index": 5,
                "rain_mm": 0.0,
            },
            "operational_status": "operational",
        }

    def test_create_weather_data(self):
        response = self.client.post(self.create_url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify data in the database
        weather_data = WeatherMasterXData.objects.get(station_identifier="ST123")
        self.assertEqual(weather_data.location.city_name, "Sample City")
        self.assertEqual(weather_data.location.coordinates.lat, 45.0)
        self.assertEqual(weather_data.location.coordinates.lon, -93.0)
        self.assertEqual(weather_data.readings.temp_fahrenheit, 75.5)
        self.assertEqual(weather_data.readings.humidity_percent, 60.0)
        self.assertEqual(weather_data.readings.pressure_hpa, 1013)
        self.assertEqual(weather_data.operational_status, "operational")

    def test_create_weather_data_invalid_data(self):
        invalid_data = self.data.copy()
        invalid_data.pop("station_identifier")

        response = self.client.post(self.create_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("station_identifier", response.data)

    def sample_data(self):
        city_name = "Sample City"
        coordinates = Coordinates.objects.create(lat=45.0, lon=-93.0)
        location = Location.objects.create(city_name=city_name, coordinates=coordinates)
        readings = Readings.objects.create(
            temp_fahrenheit=75.5,
            humidity_percent=60.0,
            pressure_hpa=1013,
            uv_index=5,
            rain_mm=0.0,
        )
        self.weather_data = WeatherMasterXData.objects.create(
            station_identifier="ST123",
            location=location,
            city=city_name,
            recorded_at="2024-11-08T12:00:00Z",
            readings=readings,
            operational_status="operational",
        )

        return self.weather_data, city_name

    def test_get_weather_data_by_city(self):
        weather_data, city_name = self.sample_data()
        response = self.client.get(self.get_url)

        serializer = WeatherMasterXDataSerializer([weather_data], many=True)

        # Check that the response is 200 OK and data matches
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_weather_data_by_city_no_data(self):
        non_existent_city_url = reverse(
            "WMX_get_weather_data_by_city", args=["NonExistentCity"]
        )
        response = self.client.get(non_existent_city_url)

        # Expecting an empty list if no data is found
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
