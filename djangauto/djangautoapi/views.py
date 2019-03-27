from django.http import HttpResponse
from django.shortcuts import render
import os

from .models import Car

def index(request):
    car_list = Car.objects.order_by('brand')
    context = {'car_list': car_list}
    return render(request, 'djangautoapi/index.html', context)

def detail(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'djangautoapi/detail.html', {'car': car})