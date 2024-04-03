import os
import gspread
import requests
import pandas as pd
from typing import List
from django.conf import settings
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import partial


def get_lat_lon(df):
    from tqdm import tqdm 
    tqdm.pandas()
    # OpenWeather has their own Geolocator but they limit me to 60 API calls a minute and 1,000 a day :( 
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['geolocation'] = df['location'].progress_apply(geocode)
    df['geo_location'] = df['location'].apply(geocode)
    df['coordinates'] = df['geo_location'].apply(lambda loc: tuple(loc.point) if loc else None)
    return df


def get_current_weather(lat, lon): 
    # r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={"Charlottesville"},{"Virginia"}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
    return r


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

def get_all_rows(doc_id="1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438"): 
    gc, authorized_user = initialize_gspread()
    sh = gc.open_by_key(doc_id)
    return sh.sheet1.get_all_values()
