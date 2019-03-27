from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Cars"),
    path('<int:carmodel_id>/', views.detail, name="model_detail")
]