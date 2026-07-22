from django.urls import path
from .views import (
    WardListView,
    WardDetailView,
    WardCreateView,
    WardUpdateView,
    WardDeleteView
)

urlpatterns = [
    path('', WardListView.as_view(), name='ward_list'),
    path('create/', WardCreateView.as_view(), name='ward_create'),
    path('<int:pk>/', WardDetailView.as_view(), name='ward_detail'),
    path('update/<int:pk>/', WardUpdateView.as_view(), name='ward_update'),
    path('delete/<int:pk>/', WardDeleteView.as_view(), name='ward_delete'),
]
