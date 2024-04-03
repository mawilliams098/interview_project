from django.shortcuts import render
from . import services
from django.http import HttpResponse

cities = services.get_all_rows()
print(cities)

def index(request):
    print(request.GET)
    return render(request, 'weather/index.html')


