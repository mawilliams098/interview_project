from django.shortcuts import render
from django.core.cache import cache
from . import services
from weather.tasks import get_city_weather_task
from django.http import HttpResponse, JsonResponse

# cache.clear()

def index(request):
    
    cities = services.get_google_sheet()
    forecast = request.GET.get('forecast', None)
    cached_data = cache.get('weather')

    # Call filter function if cache is already loaded up, otherwise call filter in task
    if cached_data and forecast:
        context = {}
        context['weather'] = services.filter_results(cached_data, forecast)
        context['task_id'] = cache.get('task_id')

    # The user submitted the form without selecting an option from the dropdown menu
    elif cached_data and not forecast:
            context = {}
            context['weather'] = cached_data
            context['task_id'] = cache.get('task_id')
            return render(request, 'weather/index.html', context)
    
    # The user submitted a blank form while the data was still coming in 
    elif cache.get('task_id') and not forecast and not cached_data:
        context = {}
        context['task_id'] = cache.get('task_id')
        return render(request, 'weather/index.html', context)

    else: 
        # Celery fetches weather data asynchronously
        result = get_city_weather_task.delay(cities)
        context = {'task_id': result.task_id}
        # Need to save the task ID so that the loading bar can render each time
        cache.set('task_id', result.task_id)
    
    if forecast: 
        context['forecast'] = forecast.lower()
    
    print(forecast)
    print(context)
    
    return render(request, 'weather/index.html', context)



