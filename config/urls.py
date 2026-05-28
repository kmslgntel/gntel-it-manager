from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 인증
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 대시보드
    path('', core_views.dashboard, name='dashboard'),

    # 앱별 URL
    path('assets/', include('assets.urls')),
    path('switches/', include('switches.urls')),
    path('inspection/', include('inspection.urls')),
    path('accounts-work/', include('accounts_work.urls')),
    path('logs/', include('core.urls')),
]
