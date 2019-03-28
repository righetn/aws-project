from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=200)
    creation_date = models.DateTimeField('creation date')

    def __str__(self):
        return self.brand


class CarModel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.car) + " " + self.model_name
