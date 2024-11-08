from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from weather_master_x.models import (
    WeatherMasterXData,
    Location,
    Coordinates,
    Readings,
)


class WeatherDataByCityTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.city_name = "Sample City"
        self.url = reverse("ST_get_weather_data_by_city", args=[self.city_name])
        self.historical_url = reverse("ST_get_historical_data", args=[self.city_name])
        self.start_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        # Create some test data
        BulgarianMeteoProData.objects.create(
            station_identifier="ST123",
            city=self.city_name,
            latitude=42.0,
            longitude=23.0,
            recorded_at="2024-11-08T14:00:00Z",
            temperature_celsius="15.50",
            humidity_percent="75.0",
            wind_speed_kph="12.5",
            operational_status="active",
        )

        coordinates = Coordinates.objects.create(lat=48.12, lon=21.32)
        location = Location.objects.create(
            city_name=self.city_name, coordinates=coordinates
        )
        readings = Readings.objects.create(
            temp_fahrenheit=75.2,
            humidity_percent=59.0,
            pressure_hpa=1013.25,
            uv_index=2,
            rain_mm=0.0,
        )
        WeatherMasterXData.objects.create(
            station_identifier="Station1",
            location=location,
            recorded_at="2024-09-24T10:20:45Z",
            readings=readings,
            operational_status="operational",
        )

    def test_get_weather_data_by_city_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination and data
        self.assertIn("page", response.data)
        self.assertIn("pages", response.data)
        self.assertIn("total_items", response.data)
        self.assertIn("data", response.data)

        total_items = (
            BulgarianMeteoProData.objects.filter(city=self.city_name).count()
            + WeatherMasterXData.objects.filter(
                location__city_name=self.city_name
            ).count()
        )
        self.assertEqual(response.data["total_items"], total_items)

    def test_get_weather_data_by_city_no_data(self):
        no_data_url = reverse("ST_get_weather_data_by_city", args=["NonExistentCity"])
        response = self.client.get(no_data_url)

        # Expecting 200 OK with empty list for data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)
        self.assertEqual(response.data["data"], [])

    def test_get_weather_data_by_city_pagination(self):
        for i in range(10):  # Add extra records to ensure multiple pages
            BulgarianMeteoProData.objects.create(
                station_identifier=f"ST{i+100}",
                city=self.city_name,
                latitude=42.0,
                longitude=23.0,
                recorded_at=f"2024-11-08T{i:02}:00:00Z",
                temperature_celsius="20.0",
                humidity_percent="60.0",
                wind_speed_kph="10.0",
                operational_status="active",
            )

        # Request the first page
        response = self.client.get(f"{self.url}?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(len(response.data["data"]), 5)  # Only 5 items per page

        # Request the second page
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 2)
        self.assertEqual(len(response.data["data"]), 5)

    def test_get_historical_data_success(self):
        # Make a GET request with valid start_date and end_date
        response = self.client.get(
            f"{self.historical_url}?start_date={self.start_date}&end_date={self.end_date}"
        )

        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination and data
        self.assertIn("page", response.data)
        self.assertIn("pages", response.data)
        self.assertIn("total_items", response.data)
        self.assertIn("data", response.data)

        # Validate the total items count within the date range
        total_items = (
            BulgarianMeteoProData.objects.filter(
                city=self.city_name, created_at__range=[self.start_date, self.end_date]
            ).count()
            + WeatherMasterXData.objects.filter(
                location__city_name=self.city_name,
                created_at__range=[self.start_date, self.end_date],
            ).count()
        )
        self.assertEqual(response.data["total_items"], total_items)

    def test_get_historical_data_invalid_dates(self):
        # Missing start_date parameter
        response = self.client.get(f"{self.historical_url}?end_date={self.end_date}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        # Invalid date format
        response = self.client.get(
            f"{self.historical_url}?start_date=invalid&end_date={self.end_date}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_historical_data_no_data_in_date_range(self):
        # Date range with no records
        start_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
        end_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        response = self.client.get(
            f"{self.historical_url}?start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)
        self.assertEqual(response.data["data"], [])

    def test_get_historical_data_pagination(self):
        self.start_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        for i in range(10):
            created_at = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            data = BulgarianMeteoProData.objects.create(
                station_identifier=f"ST{i+200}",
                city=self.city_name,
                latitude=42.0,
                longitude=23.0,
                recorded_at="2024-11-08T14:00:00Z",
                temperature_celsius="20.0",
                humidity_percent="60.0",
                wind_speed_kph="10.0",
                operational_status="active",
            )
            data.created_at = created_at
            data.save()

        # Request the first page
        response = self.client.get(
            f"{self.historical_url}?start_date={self.start_date}&end_date={self.end_date}&page=1"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(len(response.data["data"]), 5)  # 5 items per page

        # Request the second page
        response = self.client.get(
            f"{self.historical_url}?start_date={self.start_date}&end_date={self.end_date}&page=2"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 2)
        self.assertEqual(len(response.data["data"]), 5)
