from django.urls import path
from .views import (
    HospitalListView,
    HospitalDetailView,
    HospitalCreateView,
    HospitalUpdateView,
    HospitalDeleteView
)

urlpatterns = [
    path('', HospitalListView.as_view(), name='hospital_list'),
    path('create/', HospitalCreateView.as_view(), name='hospital_create'),
    path('<int:pk>/', HospitalDetailView.as_view(), name='hospital_detail'),
    path('update/<int:pk>/', HospitalUpdateView.as_view(), name='hospital_update'),
    path('delete/<int:pk>/', HospitalDeleteView.as_view(), name='hospital_delete'),
]
