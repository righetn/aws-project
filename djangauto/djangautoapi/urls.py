from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('models/', views.models, name="Models")
]