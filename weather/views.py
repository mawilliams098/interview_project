from django.shortcuts import render
from . import services
from django.http import HttpResponse

# grab data from APIs ONE TIME
# then on each button click just slice it a different way 
x = {'hi':'caitlin'}
print(x)

def index(request):
    # lat, lon = services.get_lat_lon("Charlottesville", "VA", "United States")
    # context = services.get_current_weather(lat, lon)
    # print(context)
    print(request.GET)
    # get_filtered_cities(request.GET['forecast'][0])
    return render(request, 'weather/index.html')


