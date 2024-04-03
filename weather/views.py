from django.shortcuts import render
from django.core.cache import cache
from . import services
from django.http import HttpResponse, JsonResponse

def get_all_weather():
    return None

def index(request):
    cities = services.get_google_sheet()
    weather = services.get_city_weather(cities)
    return render(request, 'weather/index.html')


# make separate view for wether results that fetches that data / inherits it's own index from the 
# index template? 
# current code 


