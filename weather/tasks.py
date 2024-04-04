import os
import time
import requests
from celery import shared_task
from django.core.cache import cache


@shared_task()
def get_city_weather_task(cities): 
    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
    city_weather = {}
    num_cities = len(cities)
    for i in range(len(cities)): 
        # cities is a list of lists where city[0] = city, city[1] = state
        key = cities[i][0] + ", " + cities[i][1]
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cities[i][0]},{cities[i][1]}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
        city_weather[key] = r
        cache.set('weather', city_weather, timeout=3600)
        # OpenWeather allows max 60 queries / minute for their free account
        time.sleep(1)

    cache.set('weather', city_weather, timeout=3600)
    return city_weather