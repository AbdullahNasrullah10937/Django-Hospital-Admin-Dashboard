from django import forms
from .models import Ward
from hospitals.models import Hospital


class WardForm(forms.ModelForm):
    """
    Form for Creating and Updating Ward entities.
    """
    class Meta:
        model = Ward
        fields = ['ward_name', 'capacity', 'hospital']
        widgets = {
            'ward_name': forms.TextInput(attrs={
                'class': 'w-full border border-outline-variant rounded px-3 py-2 bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary font-body-md text-body-md shadow-sm transition-all',
                'placeholder': 'e.g. Cardiac ICU'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'w-full pl-10 border border-outline-variant rounded px-3 py-2 bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary font-body-md text-body-md shadow-sm transition-all',
                'placeholder': 'e.g. 24',
                'min': '1',
                'max': '500'
            }),
            'hospital': forms.Select(attrs={
                'class': 'w-full appearance-none border border-outline-variant rounded px-3 py-2 bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary font-body-md text-body-md shadow-sm transition-all cursor-pointer'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.all()
        self.fields['hospital'].empty_label = "Select a hospital facility..."
