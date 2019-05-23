""" views """
import os

from datetime import datetime

from django.http import Http404
from django.shortcuts import render

from google_images_search import GoogleImagesSearch

from .models import Car
from .models import CarModel
from .models import CarBrand

def index(request):
    car_brand_list = CarBrand.objects.order_by('name')
    context = {'car_brand_list': car_brand_list}
    return render(request, 'djangautoapi/index.html', context)

def brand_detail(request, brand_id):
    try:
        car_model_list = CarModel.objects.filter(brand=brand_id).order_by('name')
        car_brand = CarBrand.objects.get(id=brand_id)
        context = {'car_brand':car_brand, 'car_model_list': car_model_list}
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'djangautoapi/brand_detail.html', context)

def model_detail(request, brand, model_name):
    try:
        print(model_name)
        carmodel = CarModel.objects.get(model_name = model_name)
        directory = './static/voitures/' + brand + '/' + model_name + '/'
        if not os.path.exists(directory):
            gis = GoogleImagesSearch('AIzaSyDL-iX9_5bYDWB5BHzXuMcV7xHt4_7X2JM', '003405953032685171249:uzag_hgt6fs')
            gis.search({'q': str(carmodel), 'num': 3})
            print(str(carmodel))
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
        brand_name = brand_name.replace(' ', '_')
        if CarBrand.objects.filter(name=brand_name) is not None:
            return index(request)
        car_brand = CarBrand(name=brand_name)
        car_brand.save()
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    else:
        return index(request)

def add_model(request, brand_name):
    try:
        model_name = request.POST['model_name']
        model_name = model_name.replace(' ', '_')
        car_brand = CarBrand.objects.get(name=brand_name)
        car_model = CarModel(brand=car_brand, model_name=model_name)
        car_model.save()
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    else:
        return brand_detail(request, brand_name)
