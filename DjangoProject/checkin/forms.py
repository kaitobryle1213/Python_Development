from django import forms
from .models import Company, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Form for managing the list of companies
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact_person']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional Contact Person'}),
        }

class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label="Is Admin (Manager)")
    employee_id = forms.CharField(max_length=50, required=False, help_text="Employee ID Number")
    
    field_order = ['username', 'employee_id', 'first_name', 'last_name', 'email', 'is_staff']

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
            # Update the profile (created by signal)
            if hasattr(user, 'userprofile'):
                user.userprofile.employee_id = self.cleaned_data.get('employee_id')
                user.userprofile.save()
        return user

class UserEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False, label="Is Admin (Manager)")
    employee_id = forms.CharField(max_length=50, required=False, help_text="Employee ID Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep current password'}),
        label="New Password"
    )
    
    field_order = ['username', 'employee_id', 'first_name', 'last_name', 'email', 'new_password', 'is_staff', 'is_active']

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(UserEditForm, self).__init__(*args, **kwargs)
        
        # Load initial employee_id from profile
        if self.instance.pk and hasattr(self.instance, 'userprofile'):
            self.fields['employee_id'].initial = self.instance.userprofile.employee_id
        
        if self.request_user:
            # If the user is NOT an admin (is_staff=False), they are a standard user
            if not self.request_user.is_staff:
                # Standard User Rules:
                # Can update: password (new_password), email
                # Cannot update: username, full_name (first_name, last_name), employee_id
                
                fields_to_remove = ['username', 'first_name', 'last_name', 'is_staff', 'is_active', 'employee_id']
                for field in fields_to_remove:
                    if field in self.fields:
                        del self.fields[field]
            
            else:
                # Admin Rules:
                # Cannot update: username of the employee.
                # Rest updatable.
                
                # Disable username field for admins too as per requirement
                if 'username' in self.fields:
                    self.fields['username'].disabled = True
                    self.fields['username'].help_text = "Username cannot be changed."
    
    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        
        # Handle password change
        new_pwd = self.cleaned_data.get('new_password')
        if new_pwd:
            user.set_password(new_pwd)
            
        if commit:
            user.save()
            # Save employee_id to profile
            if hasattr(user, 'userprofile') and 'employee_id' in self.cleaned_data:
                user.userprofile.employee_id = self.cleaned_data.get('employee_id')
                user.userprofile.save()
        return user
