from django.urls import path
from .views import (
    DirectorListView,
    DirectorDetailView,
    DirectorCreateView,
    DirectorUpdateView,
    DirectorDeleteView
)

urlpatterns = [
    path('', DirectorListView.as_view(), name='director_list'),
    path('create/', DirectorCreateView.as_view(), name='director_create'),
    path('<int:pk>/', DirectorDetailView.as_view(), name='director_detail'),
    path('update/<int:pk>/', DirectorUpdateView.as_view(), name='director_update'),
    path('delete/<int:pk>/', DirectorDeleteView.as_view(), name='director_delete'),
]
