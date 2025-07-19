from django import forms
from django_countries.widgets import CountrySelectWidget

from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'country', 'current_weight', 'goal']
        widgets = {
            'age': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age',
            'min': 1
        }),
        'country': CountrySelectWidget(attrs={
            'class': 'form-select country-select',
            'data-flags': 'true'
        }),
        'current_weight': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 75.5',
            'input-mode': 'decimal',
            'step': 'any'
        }),
        'goal': forms.Select(attrs={
            'class': 'form-select'
        }),
        }
    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            for filed in self.fields.values():
                filed.required = True
