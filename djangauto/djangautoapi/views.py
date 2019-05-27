""" views """
import os

from datetime import datetime

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from google_images_search import GoogleImagesSearch

from .models import Car
from .models import CarModel
from .models import CarBrand

from .forms import AddBrandForm, AddModelForm, ConnectionForm, RegistrationForm

def connection(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            print(user)
            if user is not None:
                # car_brand_list = CarBrand.objects.order_by('name')
                # context = {'car_brand_list': car_brand_list, 'form': AddBrandForm()}
                return redirect('brand_list')
            else:
                return render(request, 'djangautoapi/connection.html', context={'form': ConnectionForm()})
            
    return render(request, 'djangautoapi/connection.html', context={'form': ConnectionForm()})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            user.save()
            return render(request, 'djangautoapi/connection.html', context={'form': ConnectionForm()})

    return render(request, 'djangautoapi/registration.html', context={'form': RegistrationForm()})

def brand_list(request):
    if request.method == 'POST':
        form = AddBrandForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand_name']
            brand_name = brand_name.replace(' ', '_')
            try:
                CarBrand.objects.get(name=brand_name)
            except CarBrand.DoesNotExist:
                car_brand = CarBrand(name=brand_name)
                car_brand.save()
            return redirect('brand_list')
    else:
        car_brand_list = CarBrand.objects.order_by('name')
        print(len(car_brand_list))
        context = {'car_brand_list': car_brand_list, 'form': AddBrandForm()}
        return render(request, 'djangautoapi/brand_list.html', context)

def brand_detail(request, brand_name):
    if request.method == 'POST':
        form = AddModelForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand_name']
            model_name = form.cleaned_data['model_name']
            model_name = model_name.replace(' ', '_')
            production_year = form.cleaned_data['production_year']

            # insert brand
            try:
                car_brand = CarBrand.objects.get(name=brand_name)
            except CarBrand.DoesNotExist:
                car_brand = CarBrand(name=brand_name)
                car_brand.save()

            # insert model
            try:
                CarModel.objects.get(name=model_name, production_year=production_year)
            except CarModel.DoesNotExist:
                car_model = CarModel(brand=car_brand, name=model_name, production_year=production_year)
                car_model.save()
            return redirect('brand_detail', brand_name=brand_name)
    try:
        car_brand = CarBrand.objects.get(name=brand_name)
        car_model_list = CarModel.objects.filter(brand=car_brand.id).order_by('name')
        context = {
            'brand_name': brand_name,
            'car_model_list': car_model_list,
            'form': AddModelForm()
        }
    except CarBrand.DoesNotExist:
        raise Http404("Car brand does not exist")
    return render(request, 'djangautoapi/brand_detail.html', context)

def model_detail(request, brand_name, model_name):
    try:
        print(model_name)
        car_model = CarModel.objects.filter(name=model_name)[0]
        directory = './static/voitures/' + brand_name + '/' + model_name + '/'
        if not os.path.exists(directory):
            gis = GoogleImagesSearch('AIzaSyDL-iX9_5bYDWB5BHzXuMcV7xHt4_7X2JM', '003405953032685171249:uzag_hgt6fs')
            gis.search({'q': str(car_model), 'num': 3})
            print(str(car_model))
            for image in gis.results():
                image.download(directory)
                image.resize(500, 500)
            for root, dirs, files in os.walk(directory):
                i = 0
                for filename in files:
                    os.rename(directory + filename, directory + 'voiture' + str(i) + '.jpg')
                    i += 1

        context = {'car_model': car_model, 'brand': brand_name}
    except CarModel.DoesNotExist:
        raise Http404("CarModel does not exist")
    return render(request, 'djangautoapi/model_detail.html', context)
