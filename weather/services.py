import os
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
    # The first row is [City, State] so skip that
    return sh.sheet1.get_all_values()[1:]

def convert_weather_code(weather_code): 
    if 200 <= weather_code <= 232: 
        return "thunderstorm"
    if 300 <= weather_code <= 321:
        return "drizzle"
    if 500 <= weather_code <= 531:
        return "rain"
    if 600 <= weather_code <= 622:
        return "snow"
    if 701 <= weather_code <= 781:
        return "atmosphere"
    if weather_code == 800:
        return "clear"
    if 801 <= weather_code <= 804:
        return "clouds"
    
    return None
    

def filter_results(weather_data, forecast):

    match = {}
    res = {}

    # Grab all cities experiencing the user-selected forecast
    for city in weather_data: 
        if weather_data[city] and convert_weather_code(weather_data[city]['weather'][0]['id']) == forecast: 
            match[city] = weather_data[city]

    # Reduce that down to just the fields we need 
    for city in match: 
        fields = {}
        fields['temp'] = str(match[city]['main']['temp'])
        fields['wind'] = match[city]['wind']['speed']
        fields['weather'] = match[city]['weather'][0]['main']
        fields['weather-desc'] = match[city]['weather'][0]['description']
        res[city] = fields

    return res
