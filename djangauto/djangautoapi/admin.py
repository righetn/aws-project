from django.contrib import admin

from .models import Car
from .models import CarModel

admin.site.register(Car)
admin.site.register(CarModel)
