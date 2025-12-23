from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, BoardingHouseUser, Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['date_left', 'date_created']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean(self):
        """
        Custom validation to ensure capacity matches room type rules.
        """
        cleaned_data = super().clean()
        room_type = cleaned_data.get("room_type")
        capacity = cleaned_data.get("capacity")

        if room_type == 'Single':
            # Force capacity to 1 for single rooms
            if capacity and capacity > 1:
                self.add_error('capacity', "Single rooms can only have a capacity of 1.")
            cleaned_data['capacity'] = 1
            
        elif room_type == 'Bed Spacer':
            # Ensure bed spacers have at least 1 capacity
            if not capacity or capacity < 1:
                self.add_error('capacity', "Bed Spacer rooms must have a capacity of at least 1.")

        return cleaned_data
        

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'contact_number', 'parents_name', 'parents_contact_number', 'status', 'room', 'due_date', 'date_entry']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'parents_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent\'s Name'}),
            'parents_contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent\'s Contact Number'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.HiddenInput(),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_entry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def save(self, commit=True):
        """
        Custom save logic to automatically mark a room as 'Occupied' 
        if the number of active customers reaches the room's capacity.
        """
        customer = super().save(commit=False)
        if commit:
            customer.save()
            
            # Check if customer has a room assigned
            room = customer.room
            if room:
                # Count current active occupants in this specific room
                # (Assumes your Customer model has a 'status' field where 'Active' means staying)
                active_occupants = Customer.objects.filter(room=room, status='Active').count()
                
                # Compare occupants to room capacity
                if active_occupants >= room.capacity:
                    room.status = 'Occupied'
                    room.save()
        
        return customer        

        

class BoardingHouseUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BoardingHouseUser
        fields = ['username', 'email', 'role', 'status', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        room_type = cleaned_data.get("room_type")
        capacity = cleaned_data.get("capacity")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class BoardingHouseUserEditForm(forms.ModelForm):
    class Meta:
        model = BoardingHouseUser
        fields = ['username', 'email', 'role', 'status']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
