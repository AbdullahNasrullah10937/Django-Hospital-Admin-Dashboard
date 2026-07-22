from django import forms
from django.db import models
from .models import HospitalDirector
from hospitals.models import Hospital


class DirectorForm(forms.ModelForm):
    """
    Form for Creating and Updating HospitalDirector entities.
    Applies Bootstrap 5 widgets and filters hospital choice dropdown to available hospitals.
    """
    class Meta:
        model = HospitalDirector
        fields = ['director_name', 'qualification', 'hospital']
        widgets = {
            'director_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Dr. Sarah Jenkins',
                'required': 'required',
                'maxlength': '150'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MD, PhD, MHA',
                'required': 'required',
                'maxlength': '200'
            }),
            'hospital': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
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

    def clean_director_name(self):
        name = self.cleaned_data.get('director_name')
        if name:
            stripped = name.strip()
            if not stripped:
                raise forms.ValidationError("Director name cannot consist only of whitespace.")
            if stripped.isdigit():
                raise forms.ValidationError("Director name cannot be purely numeric.")
            return stripped
        return name

    def clean_qualification(self):
        qual = self.cleaned_data.get('qualification')
        if qual:
            stripped = qual.strip()
            if not stripped:
                raise forms.ValidationError("Qualification cannot consist only of whitespace.")
            return stripped
        return qual
