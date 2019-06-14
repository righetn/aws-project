from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path(
        "",
        LoginView.as_view(template_name="djangautoapi/connection.html"),
        name="connection",
    ),
    path("logout", LogoutView.as_view(), name="deconnection"),
    path("register", views.registration, name="registration"),
    path("model_list", views.model_list, name="model_list"),
    path("add_model", views.add_model, name="add_model"),
    path("remove_model/<int:car_model_pk>", views.remove_model, name="remove_model"),
    path("edit_model/<int:car_model_pk>", views.edit_model, name="edit_model"),
    path("car_list/<int:car_model_pk>", views.car_list, name="car_list"),
    path("add_car/<int:car_model_pk>", views.add_car, name="add_car"),
    path(
        "remove_car/<int:car_model_pk>/<int:car_pk>",
        views.remove_car,
        name="remove_car",
    ),
    path("edit_car/<int:car_model_pk>/<int:car_pk>", views.edit_car, name="edit_car"),
    path("plus_car/<int:car_model_pk>", views.plus_car, name="plus_car"),
    path("minus_car/<int:car_model_pk>", views.minus_car, name="minus_car"),
    path("car_detail/<int:car_pk>", views.car_detail, name="car_detail"),
]
