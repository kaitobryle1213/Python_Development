from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class BoardingHouseUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Room(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Occupied', 'Occupied'),
    )
    TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Bed Spacer', 'Bed Spacer'),
    )

    @property
    def occupancy_percent(self):
        """Calculates occupancy percentage for the progress bar."""
        if not self.capacity or self.capacity == 0:
            return 0
        # This 'active_customers_count' comes from the view annotation below
        count = getattr(self, 'active_customers_count', 0)
        return min(int((count / self.capacity) * 100), 100)

    room_number = models.CharField(max_length=50, unique=True, verbose_name="Room No.")
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    room_type = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Bed Spacer', 'Bed Spacer')])
    capacity = models.IntegerField(default=1) # How many people can occupy
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Room Price")
    date_created = models.DateField(auto_now_add=True) # Added for record keeping
    date_left = models.DateField(null=True, blank=True) # New field
    

    def __str__(self):
        return f"{self.room_number} - {self.room_type}"

        

class Customer(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Non-Student', 'Non-Student'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    customer_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # This is the critical connection:
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    due_date = models.DateField(null=True, blank=True)
    date_left = models.DateField(null=True, blank=True)
    date_entry = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    due_date = models.DateField()
    previous_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateField(null=True, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.due_date}"
