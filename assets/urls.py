from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    # IP 관리
    path('ip/', views.ip_list, name='ip_list'),
    path('ip/export/', views.ip_export, name='ip_export'),
    path('ip/person-search/', views.ip_person_search, name='ip_person_search'),
    path('ip/<int:pk>/', views.ip_detail, name='ip_detail'),
    path('ip/<int:pk>/edit/', views.ip_update, name='ip_update'),
    path('ip/<int:pk>/delete/', views.ip_delete, name='ip_delete'),

    # 전화번호 관리
    path('phone/', views.phone_list, name='phone_list'),
]
