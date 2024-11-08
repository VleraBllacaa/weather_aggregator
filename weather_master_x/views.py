from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import WeatherMasterXData
from .serializers import WeatherMasterXDataSerializer


@api_view(["POST"])
def create_weather_data(request):
    """
    Create a new weather data entry for WeatherMasterX type

    **Endpoint**: POST /weather_master_x/weather-data/

    ### Request Body
    ```json
    {
        "station_identifier": "Station1",
        "location": {
            "city_name": "Some City",
            "coordinates": {
                "lat": 48.12,
                "lon": 21.32
            }
        },
        "recorded_at": "2024-09-24T10:20:45Z",
        "readings": {
            "temp_fahrenheit": 75,
            "humidity_percent": 59.0,
            "pressure_hpa": 12.5,
            "uv_index": 2,
            "rain_mm": 0.0
        },
        "operational_status": "operational" OR "maintenance"
    }
    ```

    ### Response Example
    ```json
    {
        "station_identifier": "Station1",
        "location": {
            "city_name": "Some City",
            "coordinates": {
                "lat": 48.12,
                "lon": 21.32
            }
        },
        "recorded_at": "2024-09-24T10:20:45Z",
        "readings": {
            "temp_fahrenheit": 75,
            "humidity_percent": 59.0,
            "pressure_hpa": 12.5,
            "uv_index": 2,
            "rain_mm": 0.0
        },
        "operational_status": "operational" OR "maintenance"
    }
    ```
    """
    serializer = WeatherMasterXDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_weather_data_by_city(request, city_name):
    """
    List all weather data entries for a specific city

    **Endpoint**: GET /weather_master_x/weather-data/{city_name}/

    ### Response Example

    ```json
    [
        {
        "station_identifier": "Station1",
        "location": {
            "city_name": "Some City",
            "coordinates": {
                "lat": 48.12,
                "lon": 21.32
            }
        },
        "recorded_at": "2024-09-24T10:20:45Z",
        "readings": {
            "temp_fahrenheit": 75,
            "humidity_percent": 59.0,
            "pressure_hpa": 12.5,
            "uv_index": 2,
            "rain_mm": 0.0
        },
        "operational_status": "operational" OR "maintenance"
    }
    ]
    """
    weather_data = WeatherMasterXData.objects.filter(city=city_name).select_related(
        "location", "readings", "location__coordinates"
    )
    serializer = WeatherMasterXDataSerializer(weather_data, many=True)
    return Response(serializer.data)
