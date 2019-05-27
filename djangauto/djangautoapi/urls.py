from django.urls import path

from . import views

urlpatterns = [
    path('', views.connection, name="connection"),
    path('register', views.registration, name='registration'),
    path('model_list', views.model_list, name='model_list'),
    path('add_model', views.add_model, name="add_model"),
    path('brand-<str:brand_name>/model-<str:model_name>/', views.model_detail, name="model_detail"),
]
