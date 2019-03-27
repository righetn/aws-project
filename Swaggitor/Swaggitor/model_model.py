from django.db import models

class Model(models.Model):
    brand = models.ForeignKey(Car, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=200)