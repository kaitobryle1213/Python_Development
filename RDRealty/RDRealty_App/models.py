from django.db import models
from django.utils import timezone
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User
import os

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
        db_index=True,
    )

    title_status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='ACT',
        verbose_name="Status",
        db_index=True,
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
        verbose_name="Date Added",
        db_index=True,
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

class PropertyHistory(models.Model):
    CHANGE_TYPES = [
        ('ADD', 'Add'),
        ('UPDATE', 'Update'),
        ('STATUS_CHANGE', 'Status Change'),
        ('TAX_UPDATE', 'Tax Update'),
        ('MOVEMENT_UPDATE', 'Movement Update'),
    ]

    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE,
        related_name='history'
    )
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, default='UPDATE')
    reason = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rdrealty_property_history'
        ordering = ['-changed_at']

    def __str__(self):
        return f"Change in {self.field_name} for {self.property.title_no} at {self.changed_at}"

# --- 10. AI REQUEST LOG ---
class AIRequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_type = models.CharField(max_length=50, default='chat') 

    def __str__(self):
        return f"AI Request at {self.timestamp}"

    class Meta:
        verbose_name = "AI Request Log"
        verbose_name_plural = "AI Request Logs"

class TitleMovementRequest(models.Model):
    tm_purpose = models.CharField(max_length=200, verbose_name="Purpose of Release")
    tm_transmittal_no = models.CharField(max_length=20, verbose_name="Transmittal Number")
    tm_received_by = models.CharField(max_length=60, verbose_name="Received By")
    tm_turned_over_by = models.CharField(max_length=60, null=True, blank=True, verbose_name="Turned Over By")
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE,
        related_name='title_movements'
    )
    tm_released_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='released_movements',
        verbose_name="Released By"
    )
    tm_approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_movements',
        verbose_name="Approved By"
    )
    STATUS_CHOICES = [
        ('Released', 'Released'),
        ('In Transit', 'In Transit'),
        ('Received', 'Received'),
        ('Returned', 'Returned'),
        ('Lost', 'Lost'),
        ('Pending Return', 'Pending Return'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Released')
    tm_returned_by = models.CharField(max_length=60, null=True, blank=True, verbose_name="Returned By")
    tm_received_by_on_return = models.CharField(max_length=60, null=True, blank=True, verbose_name="Received By (On Return)")
    returned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rdrealty_title_mov_request'

class TitleMovementDocument(models.Model):
    movement = models.ForeignKey(
        TitleMovementRequest,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField(upload_to='movement_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rdrealty_title_mov_docs'

class LocalInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    loc_specific = models.TextField(blank=True, null=True)
    loc_province = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    loc_city = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    loc_barangay = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    
    class Meta:
        db_table = 'rdrealty_local_information'
        indexes = [
            models.Index(fields=['loc_province', 'loc_city', 'loc_barangay']),
        ]

class OwnerInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    oi_fullname = models.CharField(max_length=80, blank=True, null=True, db_index=True)
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

class AdditionalInformation(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    ai_remarks = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        db_table = 'rdrealty_additional_information'


class PropertyTax(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    tax_year = models.IntegerField(verbose_name="Tax Year")
    tax_quarter = models.CharField(max_length=20, verbose_name="Quarter")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    tax_due_date = models.DateField(verbose_name="Due Date")
    tax_from = models.DateField(verbose_name="Period From")
    tax_to = models.DateField(verbose_name="Period To")
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Due', 'Due'),
        ('Overdue', 'Overdue'),
        ('Paid', 'Paid'),
        ('Partially Paid', 'Partially Paid'),
        ('Contested', 'Contested'),
        ('Exempted', 'Exempted'),
        ('Waived', 'Waived'),
    ]
    tax_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Status")
    tax_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Remarks")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tax_records_created'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'rdrealty_tax_record'


def supporting_document_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    prop_id = getattr(instance, "property_id", None)
    if not prop_id and getattr(instance, "property", None):
        prop_id = getattr(instance.property, "property_id", "")
    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d")
    safe_base = base.replace(" ", "_")
    return f"supporting_docs/{safe_base}_{prop_id}_{timestamp}{ext}"


class SupportingDocument(models.Model):
    property = models.ForeignKey(
        Property,
        to_field='property_id',
        db_column='property_id',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=supporting_document_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rdrealty_supporting_documents'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('PROPERTY', 'Property'),
        ('USER', 'User'),
        ('TAX', 'Tax Record'),
        ('MOVEMENT', 'Title Movement'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    read_by = models.ManyToManyField(User, related_name='read_notifications', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
