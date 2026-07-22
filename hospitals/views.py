from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Hospital
from .forms import HospitalForm
from directors.models import HospitalDirector
from wards.models import Ward


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Custom Admin Dashboard View.
    Displays network statistics: Total Hospitals, Total Directors, Total Wards,
    and recent activity records.
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_hospitals'] = Hospital.objects.count()
        context['total_directors'] = HospitalDirector.objects.count()
        context['total_wards'] = Ward.objects.count()
        
        # Recent activities dynamically assembled from recent hospital and director additions
        recent_hospitals = Hospital.objects.order_by('-hospital_id')[:3]
        recent_directors = HospitalDirector.objects.order_by('-director_id')[:3]
        recent_wards = Ward.objects.order_by('-ward_id')[:3]
        
        context['recent_hospitals'] = recent_hospitals
        context['recent_directors'] = recent_directors
        context['recent_wards'] = recent_wards
        return context


class HospitalListView(LoginRequiredMixin, ListView):
    """
    ListView for Hospital Entity.
    Supports search by hospital name or location, and pagination (5 per page).
    """
    model = Hospital
    template_name = 'hospitals/hospital_list.html'
    context_object_name = 'hospitals'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(hospital_name__icontains=query) | Q(location__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class HospitalDetailView(LoginRequiredMixin, DetailView):
    """
    DetailView for Hospital Entity.
    Displays single hospital details, its assigned director, and its wards.
    """
    model = Hospital
    template_name = 'hospitals/hospital_detail.html'
    context_object_name = 'hospital'
    pk_url_kwarg = 'pk'


class HospitalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CreateView for Hospital Entity.
    """
    model = Hospital
    form_class = HospitalForm
    template_name = 'hospitals/hospital_form.html'
    success_url = reverse_lazy('hospital_list')
    success_message = "Hospital added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class HospitalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateView for Hospital Entity.
    """
    model = Hospital
    form_class = HospitalForm
    template_name = 'hospitals/hospital_form.html'
    success_url = reverse_lazy('hospital_list')
    success_message = "Record updated successfully"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for Hospital Entity.
    """
    model = Hospital
    template_name = 'hospitals/hospital_confirm_delete.html'
    success_url = reverse_lazy('hospital_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        messages.success(self.request, "Hospital deleted successfully")
        return super().form_valid(form)
