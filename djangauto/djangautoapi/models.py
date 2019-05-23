from django.db import models

class CarBrand(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name.__str__().replace('_', ' ')

class CarModel(models.Model):
    name = models.CharField(max_length=30)
    creation_date = models.DateTimeField('creation date')
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False, default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name.__str__().replace('_', ' ')

class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    def __str__(self):
        return self.brand.__str__() + " " + self.model.__str__()