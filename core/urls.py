from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.auditlog_list, name='auditlog_list'),
]
