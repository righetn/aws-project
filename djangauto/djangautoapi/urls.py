from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('addbrand/', views.add_brand, name="add_brand"),
    path('<slug:brand>/addmodel/', views.add_model, name="add_model"),
    path('<slug:brand>/', views.brand_detail, name="brand_detail"),
    path('<slug:brand>/<slug:model_name>/', views.model_detail, name="model_detail"),
]
