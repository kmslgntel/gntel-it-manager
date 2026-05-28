from django.urls import path
from . import views

app_name = 'switches'

urlpatterns = [
    path('', views.switch_list, name='switch_list'),
    path('backups/', views.backup_list, name='backup_list'),
]
