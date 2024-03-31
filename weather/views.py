from django.shortcuts import render
from . import services

def index(request):
    return render(request, 'weather/index.html')

