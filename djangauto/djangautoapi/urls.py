from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='djangautoapi/connection.html'), name="connection"),
    path('logout', LogoutView.as_view(), name='deconnection'),
    path('register', views.registration, name='registration'),
    path('model_list', views.model_list, name='model_list'),
    path('add_model', views.add_model, name="add_model"),
    path('model_detail/<int:car_model_pk>', views.model_detail, name="model_detail")
]
