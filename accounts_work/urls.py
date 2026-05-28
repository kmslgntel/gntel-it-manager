from django.urls import path
from . import views

app_name = 'accounts_work'

urlpatterns = [
    path('', views.accountwork_list, name='list'),
]
