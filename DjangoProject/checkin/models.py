# checkin/models.py

from django.db import models
from decimal import Decimal

# --- MODEL: Company ---
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name

# --- MODEL: CheckIn (Fixed) ---
class CheckIn(models.Model):
    # Field 1: The employee's main company
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employee_checkins',
        verbose_name="Employee's Company"
    )

    # Field 2: The current location (links to the same Company model)
    current_location = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='location_checkins',
        verbose_name="Current Company Location"
    )

    # Employee Information
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)

    # Location Data
    location_lat = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        verbose_name="Latitude"
    )
    location_lon = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        verbose_name="Longitude"
    )

    # Photo/Selfie
    selfie_photo = models.ImageField(
        upload_to='selfies/%Y/%m/%d/',
        verbose_name="Selfie Photo"
    )

    # Submission Metadata
    # CRITICAL CHANGE: Removed auto_now_add=True
    # The view will now pass the client's time directly to this field.
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Personnel Check-In"
        verbose_name_plural = "Personnel Check-Ins"

    def __str__(self):
        return f"{self.employee_name} ({self.company.name}) - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"