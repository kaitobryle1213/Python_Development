from django.db import models
from django.contrib.auth.models import AbstractUser

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

    room_number = models.CharField(max_length=50, unique=True, verbose_name="Room No.")
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    room_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Room Type")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Room Price")

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
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    address = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    customer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    room_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Room No. (Legacy)")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    due_date = models.DateField(null=True, blank=True)

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
