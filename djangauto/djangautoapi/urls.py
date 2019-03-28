from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('addbrand/', views.add_brand, name="add_brand"),
    path('brand-<str:brand>/addmodel/', views.add_model, name="add_model"),
    path('brand-<str:brand>/', views.brand_detail, name="brand_detail"),
    path('brand-<str:brand>/model-<str:model_name>/', views.model_detail, name="model_detail"),
]
