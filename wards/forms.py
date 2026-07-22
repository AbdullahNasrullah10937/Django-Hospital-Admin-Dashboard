from django import forms
from .models import Ward
from hospitals.models import Hospital


class WardForm(forms.ModelForm):
    """
    Form for Creating and Updating Ward entities.
    Applies Bootstrap 5 widgets and server-side validators.
    """
    class Meta:
        model = Ward
        fields = ['ward_name', 'capacity', 'hospital']
        widgets = {
            'ward_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Cardiac ICU',
                'required': 'required',
                'maxlength': '150'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 24',
                'required': 'required',
                'min': '1',
                'max': '500'
            }),
            'hospital': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.all()
        self.fields['hospital'].empty_label = "Select a hospital facility..."

    def clean_ward_name(self):
        name = self.cleaned_data.get('ward_name')
        if name:
            stripped = name.strip()
            if not stripped:
                raise forms.ValidationError("Ward name cannot consist only of whitespace.")
            return stripped
        return name

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None:
            if capacity < 1 or capacity > 500:
                raise forms.ValidationError("Ward capacity must be between 1 and 500 beds.")
        return capacity
