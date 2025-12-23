from django.db import models
from django.utils import timezone # Import for default date setting
from django.db.models import Max

# --- 1. PROPERTY MODEL ---
class Property(models.Model):

    # --- Choice Definitions ---
    CLASSIFICATION_CHOICES = [
        ('RES', 'RESIDENTIAL'),
        ('COM', 'COMMERCIAL'),
        ('IND', 'INDUSTRIAL'),
        ('AGR', 'AGRICULTURAL'),
        ('MIX', 'MIXED USE'),
        ('INS', 'INSTITUTIONAL'),
    ]

    STATUS_CHOICES = [
        ('ACT', 'ACTIVE'),
        ('COL', 'COLLATERAL'),
        ('SOLD', 'SOLD'),
        ('UND', 'UNDER DEVELOPMENT'),
        ('FORC', 'FORECLOSED'),
        ('DISP', 'DISPOSED'),
        ('PENT', 'PENDING TRANSFER'),
        ('INT', 'INACTIVE'),
    ]

    # --- Fields ---
    title_no = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Title Number",
        help_text="Official title certificate number",
    )

    lot_no = models.CharField(
        max_length=100,
        verbose_name="Lot Number",
        help_text="Lot identification number",
    )

    lot_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Lot Area (sqm)",
        help_text="Total area in square meters",
    )

    title_classification = models.CharField(
        max_length=3,
        choices=CLASSIFICATION_CHOICES,
        default='RES',
        verbose_name="Classification",
    )

    title_status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='ACT',
        verbose_name="Status",
    )

    title_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional property description",
    )
    
    # NEW FIELD: For monthly property count metric
    date_added = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date Added"
    )
    
    property_id = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True
    )
    
    user_id = models.PositiveIntegerField(
        default=1
    )

    # --- Model Metadata ---
    def __str__(self):
        return f"Property: {self.title_no} ({self.lot_no})"
    
    def save(self, *args, **kwargs):
        if self.property_id is None:
            last = Property.objects.aggregate(Max('property_id'))['property_id__max'] or 0
            self.property_id = last + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

# The TitleMovement and PropertyTax models have been removed.

class LocalInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    loc_specific = models.TextField(blank=True, null=True)
    loc_province = models.CharField(max_length=255, blank=True, null=True)
    loc_city = models.CharField(max_length=255, blank=True, null=True)
    loc_barangay = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'rdrealty_local_information'

class OwnerInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    oi_fullname = models.CharField(max_length=80, blank=True, null=True)
    oi_bankname = models.CharField(max_length=50, blank=True, null=True)
    oi_custody_title = models.CharField(max_length=60, blank=True, null=True)
    
    class Meta:
        db_table = 'rdrealty_owner_information'

class FinancialInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    fi_encumbrance = models.CharField(max_length=250, blank=True, null=True)
    fi_mortgage = models.CharField(max_length=150, blank=True, null=True)
    fi_borrower = models.CharField(max_length=80, blank=True, null=True)
    
    class Meta:
        db_table = 'rdrealty_financial_information'
