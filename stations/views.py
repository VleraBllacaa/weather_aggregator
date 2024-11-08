from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from weather_master_x.models import WeatherMasterXData
from .serializers import UnifiedWeatherDataSerializer
from django.utils.dateparse import parse_date
from datetime import datetime


@api_view(["GET"])
def get_weather_data_by_city(request, city_name):
    """
    Retrieve paginated weather data for a specific city
    regardless of station type.

    **Endpoint**: GET /stations/weather-data/{city_name}/

    ### Response Example
    ```json
    {
        "page": 1,
        "pages": 1,
        "total_items": 5,
        "weather_data": [
            {
                "station_id": "ST123",
                "city": "Sample City",
                "latitude": 42.0,
                "longitude": 23.0,
                "timestamp": "2024-11-08T14:00:00Z",
                "temperature_celsius": "15.50",
                "temperature_fahrenheit": "59.90",
                "humidity_percent": "75.00",
                "wind_speed_kph": "12.50",
                "station_status": "active",
                "operational_status": null,
                "pressure_hpa": null,
                "uv_index": null,
                "rain_mm": null
            },
            {
                "station_id": "Station1",
                "city": "Some City",
                "latitude": 48.12,
                "longitude": 21.32,
                "temperature_celsius": "24.00",
                "temperature_fahrenheit": "75.20",
                "humidity_percent": "59.00",
                "wind_speed_kph": "null",
                "pressure_hpa": "1013.25",
                "uv_index": "2",
                "rain_mm": "0.00",
                "timestamp": "2024-09-24T10:20:45Z",
                "station_status": null,
                "operational_status": "operational"
            }
        ]
    }
    ```

    """
    weather_data = []

    meteo_data = BulgarianMeteoProData.objects.filter(city=city_name)
    masterx_data = WeatherMasterXData.objects.filter(location__city_name=city_name)
    weather_data.extend(meteo_data)
    weather_data.extend(masterx_data)

    weather_data.sort(
        key=lambda x: getattr(x, "timestamp", getattr(x, "recorded_at", None))
    )

    # Paginate results
    paginator = Paginator(weather_data, 5)
    page_number = request.query_params.get("page", 1)
    page = paginator.get_page(page_number)

    # Serialize paginated data for response
    serializer = UnifiedWeatherDataSerializer(page, many=True)
    return Response(
        {
            "page": page.number,
            "pages": paginator.num_pages,
            "total_items": paginator.count,
            "data": serializer.data,
        }
    )


@api_view(["GET"])
def get_historical_data(request, city_name):
    """
    Retrieve paginated historical weather data for a specific city regardless of station type.

    **Endpoint**: GET
    /stations/historical-data/{city_name}?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD

    ### Response Example

    ```json
    {
        "page": 1,
        "pages": 1,
        "total_items": 5,
        "data": [
            {
                "station_id": "ST123",
                "city": "Sample City",
                "latitude": 42.0,
                "longitude": 23.0,
                "timestamp": "2024-11-08T14:00:00Z",
                "temperature_celsius": "15.50",
                "temperature_fahrenheit": "59.90",
                "humidity_percent": "75.00",
                "wind_speed_kph": "12.50",
                "station_status": "active",
                "operational_status": null,
                "pressure_hpa": null,
                "uv_index": null,
                "rain_mm": null
            },
            {
                "station_id": "Station1",
                "city": "Some City",
                "latitude": 48.12,
                "longitude": 21.32,
                "temperature_celsius": "24.00",
                "temperature_fahrenheit": "75.20",
                "humidity_percent": "59.00",
                "wind_speed_kph": "null",
                "pressure_hpa": "1013.25",
                "uv_index": "2",
                "rain_mm": "0.00",
                "timestamp": "2024-09-24T10:20:45Z",
                "station_status": null,
                "operational_status": "operational"
            }
        ]
    }
    """

    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    # Parse dates and ensure they are in correct format
    start_date = parse_date(start_date) if start_date else None
    end_date = parse_date(end_date) if end_date else datetime.now().date()

    if not start_date or not end_date:
        return Response(
            {"error": "Invalid or missing start_date and/or end_date."}, status=400
        )

    weather_data = []

    meteo_data = BulgarianMeteoProData.objects.filter(
        city=city_name, created_at__range=[start_date, end_date]
    )
    masterx_data = WeatherMasterXData.objects.filter(
        city=city_name, created_at__range=[start_date, end_date]
    ).select_related("location", "readings", "location__coordinates")

    weather_data.extend(meteo_data)
    weather_data.extend(masterx_data)

    paginator = Paginator(weather_data, 5)
    page_number = request.query_params.get("page", 1)
    page = paginator.get_page(page_number)

    # Serialize paginated data for response
    serializer = UnifiedWeatherDataSerializer(page, many=True)
    return Response(
        {
            "page": page.number,
            "pages": paginator.num_pages,
            "total_items": paginator.count,
            "data": serializer.data,
        }
    )
