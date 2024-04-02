from django.shortcuts import render
from . import services
from django.http import HttpResponse

def index(request):
    # lat, lon = services.get_lat_lon("Charlottesville", "VA", "United States")
    # context = services.get_current_weather(lat, lon)
    # print(context)
    print(request.GET)
    return render(request, 'weather/index.html')


