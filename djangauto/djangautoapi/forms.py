from datetime import datetime

from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import CarBrand, CarModel

class AddModelForm(forms.Form):
    brand_name = forms.CharField(label='Brand name', max_length=30, required=True)
    model_name = forms.CharField(label='Model name', max_length=50, required=True)
    production_year = forms.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: YYYY",
        required=True
    )
    price = forms.IntegerField(label='Price €',
        validators=[MinValueValidator(0)],
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(AddModelForm, self).__init__(*args, **kwargs)
        self.fields['brand_name'].queryset = CarBrand.objects.all().order_by('name')
        self.fields['model_name'].queryset = CarModel.objects.all().order_by('name')

class AddCarForm(forms.Form):
    price = forms.IntegerField(label='Price €',
        validators=[MinValueValidator(0)],
        required=True
    )
    occasion = forms.BooleanField(label='Occasion', required=False)
    number = forms.IntegerField(label='Number of cars to add', required=True)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())