from django.http import HttpResponse
from django.shortcuts import render
import os

from .models import Car

def index(request):
    car_list = Car.objects.order_by('brand')
    context = {'car_list': car_list}
    return render(request, 'djangautoapi/index.html', context)

def detail(request, carmodel_id):
    return HttpResponse("You're looking at car %s." % carmodel_id)