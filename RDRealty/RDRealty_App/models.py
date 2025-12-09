from django.db import models
from django.utils import timezone # Import for default date setting

# --- 1. PROPERTY MODEL ---
class Property(models.Model):

    # --- Choice Definitions ---
    CLASSIFICATION_CHOICES = [
        ('RES', 'RESIDENTIAL'),
        ('COM', 'COMMERCIAL'),
        ('IND', 'INDUSTRIAL'),
        ('AGR', 'AGRICULTURAL'),
    ]

    STATUS_CHOICES = [
        ('ACT', 'ACTIVE'),
        ('PND', 'PENDING'),
        ('SOLD', 'SOLD'),
        ('ARC', 'ARCHIVED'),
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

    # --- Model Metadata ---
    def __str__(self):
        return f"Property: {self.title_no} ({self.lot_no})"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

# The TitleMovement and PropertyTax models have been removed.