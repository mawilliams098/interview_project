import os
import dotenv
import time
import gspread
import requests
import pandas as pd
from typing import List
from django.conf import settings

def initialize_gspread(): 
    return gspread.oauth_from_dict(get_credentials(), get_authorization())

def get_credentials(): 
    return {
        "installed": {
            "client_id":os.getenv("CLIENT_ID"), 
            "project_id":os.getenv("PROJECT_ID"), 
            "auth_uri":os.getenv("AUTH_URI"),
            "token_uri":os.getenv("TOKEN_URI"),
            "auth_provider_x509_cert_url":os.getenv("AUTH_PROVIDER"), 
            "client_secret":os.getenv("CLIENT_SECRET"),
            "redirect_uris": os.getenv("REDIRECT_URIS"),
        }
    }

def get_authorization(): 
    return {
        "refresh_token": os.getenv("REFRESH_TOKEN"), 
         "token_uri": os.getenv("TOKEN_URI"), 
         "client_id": os.getenv("CLIENT_ID"), 
         "client_secret": os.getenv("CLIENT_SECRET"), 
         "scopes": os.getenv("SCOPES"), 
         "universe_domain": os.getenv("UNIVERSE_DOMAIN"), 
         "account": os.getenv("ACCOUNT"), 
         "expiry": os.getenv("EXPIRY")
    }

def get_google_sheet(doc_id="1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438"): 
    gc, authorized_user = initialize_gspread()
    sh = gc.open_by_key(doc_id)
    """
    SHORTENING THIS TO THE HEAD FOR TESTING!
    """
    return sh.sheet1.get_all_values()[1:10]

def get_city_weather(cities): 
    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
    city_weather = {}
    for city in cities: 
        # cities is a list of lists where city[0] = city, city[1] = state
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city[0]},{city[1]}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
        city_weather[tuple(city)] = r
        time.sleep(1)
    return city_weather
