from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import os

from .models import Car
from .models import CarModel

from google_images_search import GoogleImagesSearch

def index(request):
    car_list = Car.objects.order_by('brand')
    context = {'car_list': car_list}
    return render(request, 'djangautoapi/index.html', context)

def brand_detail(request, brand):
    try:
        car = Car.objects.get(brand = brand)
        carmodel_list = CarModel.objects.filter(car = car.id).order_by('model_name')
        context = {'car': car, 'carmodel_list': carmodel_list}
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'djangautoapi/brand_detail.html', context)

def model_detail(request, brand, model_name):
    try:
        carmodel_list = CarModel.objects.get(model_name = model_name)
        carmodel = carmodel_list 

        directory = '../static/voitures/' + brand + '/' + model_name + '/'
        if not os.path.exists(directory):
            gis = GoogleImagesSearch('AIzaSyDL-iX9_5bYDWB5BHzXuMcV7xHt4_7X2JM', '003405953032685171249:uzag_hgt6fs')
            gis.search({'q': brand + ' ' + model_name, 'num': 3})
            for image in gis.results():
                image.download(directory)
                image.resize(500, 500)
            for root, dirs, files in os.walk(directory):
                i = 0
                for filename in files:
                    os.rename(directory + filename, directory + 'voiture' + str(i) + '.jpg')
                    i += 1

        context = {'carmodel': carmodel, 'brand': brand}
    except CarModel.DoesNotExist:
        raise Http404("CarModel does not exist")
    return render(request, 'djangautoapi/model_detail.html', context)

def add_brand(request):
    try:
        brand_name = request.POST['brand_name']
        car = Car(brand = brand_name, creation_date = datetime.now())
        car.save()
    except (Car.DoesNotExist):
        raise Http404("Car does not exist")
    else:
        return index(request)

def add_model(request, brand):
    try:
        model_name = request.POST['model_name']
        car = Car.objects.get(brand = brand)
        carmodel = CarModel(car = car, model_name = model_name)
        carmodel.save()
    except (Car.DoesNotExist):
        raise Http404("Car does not exist")
    else:
        return brand_detail(request, brand)
