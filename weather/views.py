from django.shortcuts import render
from django.core.cache import cache
from . import services
from weather.tasks import get_city_weather_task
from django.http import HttpResponse, JsonResponse


def index(request):
    
    cities = services.get_google_sheet()
    forecast = request.GET.get('forecast', None)

    weather_data = {}

    cached_data = cache.get('weather')

    if cached_data:
        weather_data = cached_data
    else: 
        # Celery fetches weather data asynchronously
        weather_data = get_city_weather_task.delay(cities)
            
    print(cache.get('weather'))

    return render(request, 'weather/index.html')



