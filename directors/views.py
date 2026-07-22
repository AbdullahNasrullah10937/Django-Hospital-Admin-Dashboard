from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import HospitalDirector
from .forms import DirectorForm


class DirectorListView(LoginRequiredMixin, ListView):
    """
    ListView for Director Entity.
    Supports search by director name or qualification, and pagination (5 per page).
    """
    model = HospitalDirector
    template_name = 'directors/director_list.html'
    context_object_name = 'directors'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('hospital')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(director_name__icontains=query) | Q(qualification__icontains=query) | Q(hospital__hospital_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DirectorDetailView(LoginRequiredMixin, DetailView):
    """
    DetailView for Director Entity.
    """
    model = HospitalDirector
    template_name = 'directors/director_detail.html'
    context_object_name = 'director'
    pk_url_kwarg = 'pk'


class DirectorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CreateView for Director Entity.
    """
    model = HospitalDirector
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director_list')
    success_message = "Director added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class DirectorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateView for Director Entity.
    """
    model = HospitalDirector
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director_list')
    success_message = "Record updated successfully"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class DirectorDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for Director Entity.
    """
    model = HospitalDirector
    template_name = 'directors/director_confirm_delete.html'
    success_url = reverse_lazy('director_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        messages.success(self.request, "Director deleted successfully")
        return super().form_valid(form)
