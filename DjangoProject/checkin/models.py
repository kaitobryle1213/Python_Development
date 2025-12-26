# checkin/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# --- MODEL: UserProfile (Extension) ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Employee ID")

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Ensure profile exists even for existing users
        UserProfile.objects.get_or_create(user=instance)
        # We don't strictly need to call save() if we just did get_or_create,
        # unless there are other fields to update. For now, this is safer.
        if hasattr(instance, 'userprofile'):
             instance.userprofile.save()

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
    timestamp = models.DateTimeField(db_index=True)

    # Link to the System User (for access control)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkins',
        verbose_name="Linked User Account"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Personnel Check-In"
        verbose_name_plural = "Personnel Check-Ins"

    def __str__(self):
        return f"{self.employee_name} ({self.company.name}) - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"