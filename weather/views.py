from django.shortcuts import render
from django.core.cache import cache
from . import services
from django.http import HttpResponse, JsonResponse


def index(request):
    
    cities = services.get_google_sheet()
    forecast = request.GET.get('forecast', None)

    weather_data = {}

    print(cache.get('weather'))

    cached_data = cache.get('weather')
    if cached_data:
        weather_data = cached_data
    else: 
        weather_data = services.get_city_weather(cities)
        # Expiry time of 1 hour (60 * 60 = 3600)
        cache.set('weather', weather_data, timeout=3600)

    return render(request, 'weather/index.html')



