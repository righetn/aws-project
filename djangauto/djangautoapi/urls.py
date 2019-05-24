from django.urls import path

from . import views

urlpatterns = [
    path('', views.connection, name="connection"),
    path('register', views.register, name='registration'),
    path('brand_list', views.brand_list, name='brand_list'),
    path('brand-<str:brand_name>/', views.brand_detail, name="brand_detail"),
    path('brand-<str:brand_name>/model-<str:model_name>/', views.model_detail, name="model_detail"),
]
