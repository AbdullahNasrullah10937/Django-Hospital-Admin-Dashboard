from django import forms
from django.db import models
from .models import HospitalDirector
from hospitals.models import Hospital


class DirectorForm(forms.ModelForm):
    """
    Form for Creating and Updating HospitalDirector entities.
    Filters hospital choice dropdown to available hospitals.
    """
    class Meta:
        model = HospitalDirector
        fields = ['director_name', 'qualification', 'hospital']
        widgets = {
            'director_name': forms.TextInput(attrs={
                'class': 'block w-full rounded border border-outline-variant shadow-sm focus:border-primary focus:ring-2 focus:ring-primary/50 sm:text-sm px-3 py-2 text-on-surface placeholder:text-outline bg-surface-container-lowest transition-shadow',
                'placeholder': 'e.g. Dr. Sarah Jenkins'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'block w-full rounded border border-outline-variant shadow-sm focus:border-primary focus:ring-2 focus:ring-primary/50 sm:text-sm px-3 py-2 text-on-surface placeholder:text-outline bg-surface-container-lowest transition-shadow',
                'placeholder': 'e.g. MD, PhD, MHA'
            }),
            'hospital': forms.Select(attrs={
                'class': 'block w-full rounded border border-outline-variant shadow-sm focus:border-primary focus:ring-2 focus:ring-primary/50 sm:text-sm pl-3 pr-10 py-2 text-on-surface bg-surface-container-lowest appearance-none transition-shadow cursor-pointer'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter available hospitals: hospitals with no director, plus current instance's hospital if editing
        if self.instance and self.instance.pk:
            available_hospitals = Hospital.objects.filter(
                models.Q(director__isnull=True) | models.Q(pk=self.instance.hospital.pk)
            )
        else:
            available_hospitals = Hospital.objects.filter(director__isnull=True)

        self.fields['hospital'].queryset = available_hospitals
        self.fields['hospital'].empty_label = "Select a hospital facility..."
