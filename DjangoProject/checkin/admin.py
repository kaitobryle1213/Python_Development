# checkin/admin.py

from django.contrib import admin
from .models import CheckIn

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    # Customize what fields are displayed in the list view
    list_display = ('employee_name', 'employee_id', 'location_lat', 'location_lon', 'timestamp')
    # Add a search box
    search_fields = ('employee_name', 'employee_id')
    # Allow filtering by date
    list_filter = ('timestamp',)