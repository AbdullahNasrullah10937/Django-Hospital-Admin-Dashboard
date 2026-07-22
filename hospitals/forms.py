import datetime
from django import forms
from .models import Hospital


class HospitalForm(forms.ModelForm):
    """
    Form for Creating and Updating Hospital entities.
    Applies Bootstrap 5 form-control classes and explicit server/client validation attributes.
    """
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'location', 'founded_year']
        widgets = {
            'hospital_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., General Regional Medical Center',
                'required': 'required',
                'maxlength': '200'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Seattle, WA',
                'required': 'required',
                'maxlength': '255'
            }),
            'founded_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY',
                'required': 'required',
                'min': '1800',
                'max': str(datetime.date.today().year)
            })
        }

    def clean_hospital_name(self):
        name = self.cleaned_data.get('hospital_name')
        if name:
            stripped = name.strip()
            if not stripped:
                raise forms.ValidationError("Hospital name cannot consist only of whitespace.")
            # Check duplicate hospital name (case-insensitive) excluding current instance
            qs = Hospital.objects.filter(hospital_name__iexact=stripped)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A hospital facility with this name already exists.")
            return stripped
        return name

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location:
            stripped = location.strip()
            if not stripped:
                raise forms.ValidationError("Location cannot consist only of whitespace.")
            return stripped
        return location

    def clean_founded_year(self):
        year = self.cleaned_data.get('founded_year')
        current_year = datetime.date.today().year
        if year is not None:
            if year < 1800 or year > current_year:
                raise forms.ValidationError(f"Founded year must be between 1800 and {current_year}.")
        return year
