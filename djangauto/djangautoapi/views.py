""" views """
import os

from datetime import datetime
from io import BytesIO
from PIL import Image

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from google_images_search import GoogleImagesSearch
import cloudinary.uploader

from .models import Car, CarModel, CarBrand, CarModelImage

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
                return redirect('model_list')
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

def model_list(request):
    car_model_list = CarModel.objects.order_by('brand__name')
    image_model_list = []
    for car_model in car_model_list:
        image_model_list.append({
            'car_model': car_model,
            'image_list': CarModelImage.objects.filter(model=car_model)
        })
    context = {
        'image_model_list': image_model_list,
        'form': AddBrandForm(),
        }
    print(image_model_list[0]['image_list'])
    return render(request, 'djangautoapi/model_list.html', context)

def add_model(request):
    if request.method == 'POST':
        form = AddModelForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand_name']
            model_name = form.cleaned_data['model_name']
            model_name = model_name.replace(' ', '_')
            production_year = form.cleaned_data['production_year']
            price = form.cleaned_data['price']

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
                car_model = CarModel(brand=car_brand, name=model_name, production_year=production_year, price=price)
                car_model.save()

            # search images
            car_model = CarModel.objects.get(name=model_name, production_year=production_year)
            my_bytes_io = BytesIO()
            gis = GoogleImagesSearch('AIzaSyDL-iX9_5bYDWB5BHzXuMcV7xHt4_7X2JM', '003405953032685171249:uzag_hgt6fs')
            gis.search({'q': str(car_model), 'num': 3})
            for image in gis.results():
                my_bytes_io.seek(0)
                image.copy_to(my_bytes_io)
                my_bytes_io.seek(0)
                response = cloudinary.uploader.upload(my_bytes_io)
                my_bytes_io.flush()
                
                # insert image
                carmodelimage = CarModelImage(model=car_model, name=response['public_id'])
                carmodelimage.save()

            return redirect('model_list')
        else:
            print('form error')
            render(request, 'djangautoapi/add_model.html', context={'form': form})

    return render(request, 'djangautoapi/add_model.html', context={'form': AddModelForm()})

def model_detail(request, car_model_pk):
    car_model = CarModel.objects.get(pk=car_model_pk)
    images = CarModelImage.objects.filter(model=car_model)
    print(len(images))
    print(images[0].name)
    print(images[1].name)
    print(images[2].name)
    return render(request, 'djangautoapi/model_detail.html', context={'images': images})
