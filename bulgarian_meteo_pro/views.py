from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer


@api_view(["POST"])
def create_weather_data(request):
    """
    Create a new weather data entry for BulgarianMeteoPro type

    **Endpoint**: POST /bulgarian_meteo_pro/weather-data/

    ### Request Body
    ```json
    {
        "station_id": "ST123",
        "city": "Sample City",
        "latitude": 42.0,
        "longitude": 23.0,
        "timestamp": "2024-11-08T14:00:00Z",
        "temperature_celsius": "15.50",
        "humidity_percent": "75.00",
        "wind_speed_kph": "12.50",
        "station_status": "active"
    }
    ```

    ### Response Example
    ```json
    {
        "station_id": "ST123",
        "city": "Sample City",
        "latitude": 42.0,
        "longitude": 23.0,
        "timestamp": "2024-11-08T14:00:00Z",
        "temperature_celsius": "15.50",
        "humidity_percent": "75.00",
        "wind_speed_kph": "12.50",
        "station_status": "active"
    }
    ```
    """
    serializer = BulgarianMeteoProDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_weather_data_by_city(request, city_name):
    """
    List all weather data entries for a specific city

    **Endpoint**: GET /bulgarian_meteo_pro/weather-data/{city_name}/

    - `city_name`: Name of the city to retrieve weather data for

    ### Response Example
    ```json
    {
        "station_id": "ST123",
        "city": "Sample City",
        "latitude": 42.0,
        "longitude": 23.0,
        "timestamp": "2024-11-08T14:00:00Z",
        "temperature_celsius": "15.50",
        "humidity_percent": "75.00",
        "wind_speed_kph": "12.50",
        "station_status": "active"
    }
    """
    weather_data = BulgarianMeteoProData.objects.filter(city=city_name)
    serializer = BulgarianMeteoProDataSerializer(weather_data, many=True)
    return Response(serializer.data)
