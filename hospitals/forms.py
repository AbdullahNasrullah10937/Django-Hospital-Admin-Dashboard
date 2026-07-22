from django import forms
from .models import Hospital
import datetime


class HospitalForm(forms.ModelForm):
    """
    Form for Creating and Updating Hospital entities.
    Applies custom widgets and Tailwind CSS classes to match design specs.
    """
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'location', 'founded_year']
        widgets = {
            'hospital_name': forms.TextInput(attrs={
                'class': 'w-full pl-10 pr-4 py-2 border border-outline-variant rounded-md font-body-md text-body-md bg-surface text-on-surface focus:ring-2 focus:ring-primary-container/50 focus:border-primary-container transition-shadow',
                'placeholder': 'e.g., General Regional Medical Center'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full pl-10 pr-4 py-2 border border-outline-variant rounded-md font-body-md text-body-md bg-surface text-on-surface focus:ring-2 focus:ring-primary-container/50 focus:border-primary-container transition-shadow',
                'placeholder': 'e.g., Seattle, WA'
            }),
            'founded_year': forms.NumberInput(attrs={
                'class': 'w-full pl-10 pr-4 py-2 border border-outline-variant rounded-md font-body-md text-body-md bg-surface text-on-surface focus:ring-2 focus:ring-primary-container/50 focus:border-primary-container transition-shadow',
                'placeholder': 'YYYY',
                'min': '1800',
                'max': str(datetime.date.today().year)
            })
        }

    def clean_founded_year(self):
        year = self.cleaned_data.get('founded_year')
        current_year = datetime.date.today().year
        if year is not None:
            if year < 1800 or year > current_year:
                raise forms.ValidationError(f"Founded year must be between 1800 and {current_year}.")
        return year
