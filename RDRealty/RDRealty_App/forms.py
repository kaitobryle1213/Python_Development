from django import forms
from django.db.models import Max
from .models import Property

# --- 1. Property Creation Form ---
class PropertyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        next_id = (Property.objects.aggregate(Max('property_id'))['property_id__max'] or 0) + 1
        self.fields['property_id'].initial = next_id
        self.fields['user_id'].initial = 1
        self.fields['property_id'].widget.attrs.update({'readonly': 'readonly'})
    class Meta:
        model = Property
        fields = [
            'title_no', 
            'lot_no', 
            'lot_area', 
            'title_classification', 
            'title_status', 
            'title_description',
            'property_id',
            'user_id'
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
            'property_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'user_id': forms.NumberInput(attrs={'class': 'form-control'}),
        }

