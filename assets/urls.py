from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('ip/', views.ip_list, name='ip_list'),
    path('phone/', views.phone_list, name='phone_list'),
]
