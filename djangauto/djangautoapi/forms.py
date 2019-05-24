from datetime import datetime

from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator


class AddBrandForm(forms.Form):
    brand_name = forms.CharField(label='Brand name', max_length=30, required=True)

class AddModelForm(forms.Form):
    model_name = forms.CharField(label='Model name', max_length=50, required=True)
    production_year = forms.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: YYYY"
    )

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password')

class ConnectionForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password')