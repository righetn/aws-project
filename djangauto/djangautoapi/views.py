""" views """
from io import BytesIO

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from google_images_search import GoogleImagesSearch
import cloudinary.uploader

from .models import Car, CarModel, CarBrand, CarModelImage

from .forms import AddModelForm, RegistrationForm, AddCarForm

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.save()
                return render(request, 'djangautoapi/connection.html')

    return render(request, 'djangautoapi/registration.html', context={'form': RegistrationForm()})

@login_required
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
        }
    return render(request, 'djangautoapi/model_list.html', context)

@login_required
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

def car_list(request, car_model_pk):
    car_list = Car.objects.filter(model=car_model_pk).order_by('occasion')
    return render(request, 'djangautoapi/car_list.html', context={'car_list': car_list, 'car_model_pk': car_model_pk})

def add_car(request, car_model_pk):
    car_model = CarModel.objects.get(pk=car_model_pk)
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            for i in range(form.cleaned_data['number']):
                car = Car(
                    model=car_model,
                    price=form.cleaned_data['price'],
                    occasion=form.cleaned_data['occasion'],
                )
                car.save()

            car_list = Car.objects.filter(model=car_model_pk).order_by('occasion')
            return render(request, 'djangautoapi/car_list.html', context={'car_list': car_list, 'car_model_pk': car_model_pk})
    
    form = AddCarForm(initial={
        'price': car_model.price,
        'number': 1
        })
    return render(request, 'djangautoapi/add_car.html', context={'form': form, 'car_model_pk': car_model_pk})

@login_required
def car_detail(request, car_pk):
    car_model = CarModel.objects.get(pk=car_pk)
    images = CarModelImage.objects.filter(model=car_model)
    return render(request, 'djangautoapi/model_detail.html', context={'images': images})
