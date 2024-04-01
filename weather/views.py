from django.shortcuts import render
from . import services

def index(request):
    lat, lon = services.get_lat_lon("Charlottesville", "VA", "United States")
    context = services.get_current_weather(lat, lon)
    print(context)
    return render(request, 'weather/index.html', context)
