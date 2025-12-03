# checkin/forms.py

from django import forms
from .models import Company

# Form for managing the list of companies
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact_person']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional Contact Person'}),
        }