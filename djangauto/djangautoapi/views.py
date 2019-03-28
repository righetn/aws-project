from django.http import HttpResponse
from django.shortcuts import render

from .models import Car
from .models import CarModel

def index(request):
    car_list = Car.objects.order_by('brand')
    context = {'car_list': car_list}
    return render(request, 'djangautoapi/index.html', context)

def brand_detail(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
        carmodel_list = CarModel.objects.filter(car = car_id).order_by('model_name')
        context = {'car': car, 'carmodel_list': carmodel_list}
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'djangautoapi/brand_detail.html', context)

def model_detail(request, car_id, model_id):
    try:
        carmodel_list = CarModel.objects.filter(pk=model_id)
        carmodel = carmodel_list[0]
        context = {'carmodel': carmodel}
    except CarModel.DoesNotExist:
        raise Http404("CarModel does not exist")
    return render(request, 'djangautoapi/model_detail.html', context)