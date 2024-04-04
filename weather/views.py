from django.shortcuts import render
from django.core.cache import cache
from . import services
from weather.tasks import get_city_weather_task
from django.http import HttpResponse, JsonResponse


cache.clear()

def index(request):
    
    cities = services.get_google_sheet()
    forecast = request.GET.get('forecast', None)
    cached_data = cache.get('weather')

    # Call filter function if cache is already loaded up, otherwise call filter in task
    if cached_data and forecast:
        context = services.filter_results(cached_data, forecast)
    else: 
        # Celery fetches weather data asynchronously
        context = get_city_weather_task.delay(cities)
        # Tell the user to wait a minute until I load all the data
        context = {'status':'Loading...'}
        print("Hang on! I'm working on it!")
    
    print(context)

    return render(request, 'weather/index.html', context)



