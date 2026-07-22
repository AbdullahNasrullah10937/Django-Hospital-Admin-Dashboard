from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from hospitals.views import DashboardView

urlpatterns = [
    # Built-in Django Admin Panel
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Custom Admin Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_alias'),

    # Domain Application URLs
    path('hospitals/', include('hospitals.urls')),
    path('directors/', include('directors.urls')),
    path('wards/', include('wards.urls')),
]
