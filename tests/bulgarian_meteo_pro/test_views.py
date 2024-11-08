from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from bulgarian_meteo_pro.serializers import BulgarianMeteoProDataSerializer


class BulgarianMeteoProDataTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.create_url = reverse("BMP_create_weather_data")

        self.city_url = reverse("BMP_get_weather_data_by_city", args=["Sample City"])

        self.valid_data = {
            "station_id": "ST123",
            "city": "Sample City",
            "latitude": 42.0,
            "longitude": 23.0,
            "timestamp": "2024-11-08T14:00:00Z",
            "temperature_celsius": 15.5,
            "humidity_percent": 75.0,
            "wind_speed_kph": 12.5,
            "station_status": "active",
        }

        self.weather_data = BulgarianMeteoProData.objects.create(
            station_identifier="ST456",
            city="Sample City",
            latitude=42.0,
            longitude=23.0,
            recorded_at="2024-11-07T12:00:00Z",
            temperature_celsius="14.50",
            humidity_percent="70.0",
            wind_speed_kph="10.0",
            operational_status="active",
        )

    def test_create_weather_data_success(self):
        response = self.client.post(self.create_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in self.valid_data:
            self.assertEqual(response.data[key], self.valid_data[key])

    def test_create_weather_data_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("station_id")

        response = self.client.post(self.create_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("station_id", response.data)

    def test_get_weather_data_by_city(self):
        response = self.client.get(self.city_url)

        # Serialize expected data for comparison
        expected_data = BulgarianMeteoProDataSerializer(
            [self.weather_data], many=True
        ).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_weather_data_by_city_no_data(self):
        no_data_url = reverse("BMP_get_weather_data_by_city", args=["NonExistentCity"])
        response = self.client.get(no_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
