from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('brand-<str:brand_name>/', views.brand_detail, name="brand_detail"),
    path('brand-<str:brand_name>/model-<str:model_name>/', views.model_detail, name="model_detail"),
]
