import os
import time
import requests
from celery import shared_task
from django.core.cache import cache
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def get_city_weather_task(self, cities): 
    progress_recorder = ProgressRecorder(self)
    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
    city_weather = {}
    for i in range(len(cities)): 
        # Cities is a list of lists where city[0] = city, city[1] = state
        key = cities[i][0] + ", " + cities[i][1]
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cities[i][0]},{cities[i][1]}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
        if r['cod'] != 200: 
            city_weather[key] = None
        else:
            city_weather[key] = r
        progress_recorder.set_progress(i + 1, len(cities))
        # OpenWeather allows max 60 queries / minute for their free account
        time.sleep(1)

    # OpenWeather releases new weather data every 10 minutes, so reset cache if 10 *  60seconds have passed
    cache.set('weather', city_weather, timeout=600)
    print("All done!")
    return city_weather