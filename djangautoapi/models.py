from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarBrand(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name.__str__().replace("_", " ")


class CarModel(models.Model):
    name = models.CharField(max_length=30)
    production_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)]
    )
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False, default=0)

    def __str__(self):
        return (
            self.brand.__str__().replace("_", " ")
            + " "
            + self.name.__str__().replace("_", " ")
            + " "
            + self.production_year.__str__()
        )


class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    occasion = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.model.__str__()


class CarModelImage(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
