from django import forms
from .models import Property

# --- 1. Property Creation Form ---
class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title_no', 
            'lot_no', 
            'lot_area', 
            'title_classification', 
            'title_status', 
            'title_description'
        ]
        # ADD THIS WIDGETS SECTION:
        widgets = {
            # Standard Text/Number Inputs use 'form-control'
            'title_no': forms.TextInput(attrs={'class': 'form-control'}),
            'lot_no': forms.TextInput(attrs={'class': 'form-control'}),
            'lot_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), 
            
            # Select/Dropdowns use 'form-select'
            'title_classification': forms.Select(attrs={'class': 'form-select'}),
            'title_status': forms.Select(attrs={'class': 'form-select'}),
            
            # Textareas use 'form-control' and specific row count
            'title_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

