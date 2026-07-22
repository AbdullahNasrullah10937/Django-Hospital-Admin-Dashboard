from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Ward
from .forms import WardForm


class WardListView(LoginRequiredMixin, ListView):
    """
    ListView for Ward Entity.
    Supports search by ward name or hospital name, and pagination (5 per page).
    """
    model = Ward
    template_name = 'wards/ward_list.html'
    context_object_name = 'wards'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('hospital')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(ward_name__icontains=query) | Q(hospital__hospital_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class WardDetailView(LoginRequiredMixin, DetailView):
    """
    DetailView for Ward Entity.
    """
    model = Ward
    template_name = 'wards/ward_detail.html'
    context_object_name = 'ward'
    pk_url_kwarg = 'pk'


class WardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CreateView for Ward Entity.
    """
    model = Ward
    form_class = WardForm
    template_name = 'wards/ward_form.html'
    success_url = reverse_lazy('ward_list')
    success_message = "Ward added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class WardUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateView for Ward Entity.
    """
    model = Ward
    form_class = WardForm
    template_name = 'wards/ward_form.html'
    success_url = reverse_lazy('ward_list')
    success_message = "Record updated successfully"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class WardDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for Ward Entity.
    """
    model = Ward
    template_name = 'wards/ward_confirm_delete.html'
    success_url = reverse_lazy('ward_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        messages.success(self.request, "Ward deleted successfully")
        return super().form_valid(form)
