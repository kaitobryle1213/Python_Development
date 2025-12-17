from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Group, Permission # Import needed for explicit definition

class CustomUser(AbstractUser):
    """Custom user model for POS system"""
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_cashier = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    
    # --- FIX FOR fields.E304 CLASHES ---
    # Overriding the inherited fields to provide unique related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups", # <--- UNIQUE RELATED_NAME 1
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="customuser_permissions", # <--- UNIQUE RELATED_NAME 2
        related_query_name="customuser",
    )
    # -----------------------------------
    
    def __str__(self):
        return self.username


class Customer(models.Model):
    """Customer model"""
    # ... (rest of the Customer model remains the same)
    CUSTOMER_TYPE_CHOICES = [
        ('WALKIN', 'Walk-in'),
        ('REGULAR', 'Regular'),
        ('SUPPLIER', 'Supplier'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]
    
    customer_code = models.CharField(max_length=50, unique=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='WALKIN')
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField(blank=True)
    customer_tin = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    date_entry = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_code} - {self.customer_name}"
    
    class Meta:
        ordering = ['-date_entry', 'customer_name']


class Item(models.Model):
    """Item/Product model"""
    # ... (rest of the Item model remains the same)
    UNIT_CHOICES = [
        ('PCS', 'Piece'),
        ('BOX', 'Box'),
        ('PKG', 'Package'),
        ('KG', 'Kilogram'),
        ('LTR', 'Liter'),
        ('MTR', 'Meter'),
    ]
    
    item_code = models.CharField(max_length=50, unique=True)
    item_description = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    unit_selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_on_hand = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_code} - {self.item_description}"
    
    class Meta:
        ordering = ['item_description']


class POSTransaction(models.Model):
    """POS Transaction model"""
    # ... (rest of the POSTransaction model remains the same)
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('CANCELED', 'Canceled'),
    ]
    MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('PO', 'PO'),
        ('CHECK', 'Check'),
        ('ONLINE', 'Online Transfer'),
    ]
    
    transaction_no = models.CharField(max_length=50, unique=True)
    transaction_date = models.DateField(default=timezone.now)
    document_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    mode_of_payment = models.CharField(max_length=20, choices=MODE_CHOICES, default='CASH')
    
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255, blank=True)
    customer_address = models.TextField(blank=True)
    customer_tin = models.CharField(max_length=50, blank=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_amount_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cash_amount_change = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    check_number = models.CharField(max_length=50, blank=True)
    check_date = models.DateField(null=True, blank=True)
    check_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bank_number = models.CharField(max_length=50, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)
    online_transaction_date = models.DateField(null=True, blank=True)
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transaction_no} - {self.transaction_date}"
    
    def calculate_totals(self):
        """Calculate subtotal and grand total from line items"""
        line_items = self.poslineitem_set.all()
        self.subtotal = sum(item.subtotal for item in line_items)
        self.grand_total = self.subtotal
        self.save()
    
    class Meta:
        ordering = ['-transaction_date', '-transaction_no']


class POSLineItem(models.Model):
    """POS Transaction Line Item"""
    # ... (rest of the POSLineItem model remains the same)
    transaction = models.ForeignKey(POSTransaction, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Item, on_delete=models.PROTECT)
    item_description = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=10)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    unit_selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.transaction.transaction_no} - {self.item_code}"
    
    class Meta:
        ordering = ['id']
