from django.shortcuts import render
from django.core.cache import cache
from . import services
from weather.tasks import get_city_weather_task

# cache.clear()

def index(request):
    
    context = {}
    forecast = request.GET.get('forecast', None)
    context['task_id'] = cache.get('task_id')
    context['cache_weather'] = cache.get('data')
    context['forecast'] = forecast.lower() if forecast else None

    # If weather data was found in the cache and the user selected a condition, filter
    if context['cache_weather'] and context['forecast']:
        context['filtered_weather'] = services.filter_results(context['cache_weather'], context['forecast'])

    # The user submitted the form without selecting an option from the dropdown menu
    # OR the user submitted a blank form while the data was still coming in 
    elif (context['cache_weather'] and not context['forecast'] or 
          context['task_id'] and not context['forecast'] and not context['cache_weather']):
        return render(request, 'weather/index.html', context)
    
    # Celery fetches weather data asynchronously and saves it to cache 
    else: 
        cities = services.get_google_sheet()
        result = get_city_weather_task.delay(cities)
        # Need to keep track of the task_id at all times for loading bar 
        context['task_id'] = result.task_id
        cache.set('task_id', result.task_id)

    print(context)
      
    return render(request, 'weather/index.html', context)



