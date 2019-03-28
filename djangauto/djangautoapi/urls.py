from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('<int:car_id>/', views.brand_detail, name="brand_detail"),
    path('<int:car_id>/<int:model_id>/', views.model_detail, name="model_detail")
    path('addbrand/', views.add_brand, name="add_brand")
    path('<int:car_id>/addmodel/', views.add_model, name"add_model")
]