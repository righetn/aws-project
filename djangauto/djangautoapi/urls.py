from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('<int:car_id>/', views.brand_detail, name="brand_detail"),
    path('<int:model_detail>', views.model_detail, name="model_detail")
]