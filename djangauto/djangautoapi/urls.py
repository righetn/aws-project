from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='djangautoapi/connection.html'), name="connection"),
    path('logout', LogoutView.as_view(), name='deconnection'),
    path('register', views.registration, name='registration'),
    path('model_list', views.model_list, name='model_list'),
    path('add_model', views.add_model, name="add_model"),
    path('car_list/<int:car_model_pk>', views.car_list, name='car_list'),
    path('add_car/<int:car_model_pk>', views.add_car, name='add_car'),
    path('remove_car/<int:car_model_pk>/<int:car_pk>', views.remove_car, name='remove_car'),
    path('car_detail/<int:car_pk>', views.car_detail, name="car_detail")
]
