import os
import requests
import json
import pandas as pd
import dotenv 
dotenv.load_dotenv()

OPEN_WEATHER_KEY = os.getenv('OPEN_WEATHER_KEY')

def get_lat_lon(city_name, state_code, country_code, API_key): 
    r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data = r[0]
    lat, lon = data['lat'], data['lon']
    return lat, lon

def get_current_weather(lat, lon, API_key): 
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial').json()
    print(r)

cville_coords = get_lat_lon("Charlottesville", "VA", "United States", OPEN_WEATHER_KEY)
cville_weather = get_current_weather(cville_coords[0], cville_coords[1], OPEN_WEATHER_KEY)
print(cville_weather)