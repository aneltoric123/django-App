from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget

from .models import UserProfile, WeightEntry


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password','first_name','last_name','is_superuser','groups','user_permissions','is_staff','is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        label='New Password (leave blank to keep current)',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )




class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter today\'s weight'
            })
        }