# checkin/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckIn, Company 
from django.views.decorators.http import require_http_methods
from decimal import Decimal, InvalidOperation
from .forms import CompanyForm # Ensure this Form is defined
from django.http import HttpResponse
from .filters import CheckInFilter
import csv
from datetime import datetime
from django.urls import reverse # Required for redirects if not using name directly

# Define the exact format string matching the JavaScript output: 'Dec 03, 2025 15:50'
CLIENT_DATETIME_FORMAT = '%b %d, %Y %H:%M'


@require_http_methods(["GET", "POST"])
def checkin_view(request):
    """Handles the display and submission of the CheckIn form."""
    error_message = None
    companies = Company.objects.all()

    if request.method == 'POST':
        # 1. Retrieve data
        name = request.POST.get('employee_name')
        id_num = request.POST.get('employee_id')
        lat_str = request.POST.get('location_lat')
        lon_str = request.POST.get('location_lon')
        selfie = request.FILES.get('selfie_photo')
        company_id = request.POST.get('company_id')
        current_location_id = request.POST.get('current_location_id')

        # NEW: Retrieve the client's timestamp string
        client_timestamp_str = request.POST.get('client_timestamp')

        # 2. Validation (Updated to include current_location_id and client_timestamp_str)
        if not all([name, id_num, lat_str, lon_str, selfie, company_id, current_location_id, client_timestamp_str]):
            error_message = 'Submission failed: All fields, including the timestamp, are required.'
        else:
            try:
                # Retrieve the Company objects
                company_obj = Company.objects.get(pk=company_id)
                current_location_obj = Company.objects.get(pk=current_location_id)

                # Convert location strings to Decimal
                lat = Decimal(lat_str)
                lon = Decimal(lon_str)

                # Check for sentinel values
                if lat == Decimal('30.0') and lon == Decimal('15.0'):
                    error_message = 'Submission failed: Please click the "Find My Exact Location" button to capture your current GPS.'
                else:
                    # 3. Parse client time
                    try:
                        client_dt = datetime.strptime(client_timestamp_str, CLIENT_DATETIME_FORMAT)
                    except ValueError:
                        error_message = 'Invalid date/time format submitted.'
                        # Skip saving if parsing fails
                        raise ValueError("Timestamp parsing failed")

                    # 4. Create and Save Record
                    new_checkin = CheckIn.objects.create(
                        company=company_obj,
                        current_location=current_location_obj,
                        employee_name=name,
                        employee_id=id_num,
                        location_lat=lat,
                        location_lon=lon,
                        selfie_photo=selfie,
                        timestamp=client_dt  # CRITICAL CHANGE: Use the parsed client time
                    )
                    return redirect('checkin_success', pk=new_checkin.pk)

            except Company.DoesNotExist:
                error_message = 'Invalid Company or Location selected.'
            except (InvalidOperation, ValueError):
                error_message = 'Submission failed: Invalid location data provided or timestamp parsing error.'
            except Exception as e:
                # Catch other potential errors
                if not error_message:  # Don't overwrite specific errors above
                    error_message = f'An unexpected error occurred during save: {e}'

    # Final Render
    context = {
        'companies': companies,
        'error_message': error_message
    }
    return render(request, 'checkin/checkin_form.html', context)


# ----------------------------------------------------------------------
# EXISTING VIEW: SUCCESS PAGE (No changes needed here)
# ----------------------------------------------------------------------

def checkin_success_view(request, pk):
    record = get_object_or_404(CheckIn, pk=pk)
    context = {
        'record': record
    }
    return render(request, 'checkin/checkin_success.html', context)


# ----------------------------------------------------------------------
# EXISTING VIEW: COMPANY MANAGEMENT (No changes needed here)
# ----------------------------------------------------------------------

def company_list_view(request):
    """Handles company creation and displays existing companies."""
    form = CompanyForm()
    companies = Company.objects.all()

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')

    context = {
        'form': form,
        'companies': companies
    }
    return render(request, 'checkin/company_list.html', context)

# ----------------------------------------------------------------------
# ⭐ NEW VIEW: COMPANY EDIT/UPDATE
# ----------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def company_edit_view(request, pk):
    """Handles editing an existing Company object."""
    # Retrieve the object instance or return 404
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        # Bind request data to the form, passing the existing instance
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            # Redirect back to the list after saving
            return redirect('company_list')
    else:
        # For a GET request, initialize the form with the current instance data
        form = CompanyForm(instance=company)
    
    context = {
        'form': form,
        'company': company,
        'is_editing': True # Useful for template logic
    }
    # You need to create this template: 'checkin/company_edit.html'
    return render(request, 'checkin/company_edit.html', context)

# ----------------------------------------------------------------------
# ⭐ NEW VIEW: COMPANY DELETE
# ----------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def company_delete_view(request, pk):
    """Handles the deletion of a Company object."""
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        # Delete the object if the request is POST (confirming the action)
        company.delete()
        # Redirect back to the list after deletion
        return redirect('company_list')
    
    # For a GET request, show the confirmation template
    context = {
        'company': company
    }
    # You need to create this template: 'checkin/company_confirm_delete.html'
    return render(request, 'checkin/company_confirm_delete.html', context)


# ----------------------------------------------------------------------
# EXISTING VIEW: REPORT & FILTERING (No changes needed here)
# ----------------------------------------------------------------------

def checkin_report_view(request):
    """
    Displays the CheckIn records and allows filtering.
    """
    # Instantiate the filter using the request GET parameters
    filter = CheckInFilter(request.GET, queryset=CheckIn.objects.all().order_by('-timestamp'))

    context = {
        'filter': filter,
        'records': filter.qs  # The filtered queryset results
    }
    return render(request, 'checkin/checkin_report.html', context)


# ----------------------------------------------------------------------
# EXISTING VIEW: EXPORT TO CSV (EXCEL) (No changes needed here)
# ----------------------------------------------------------------------

def export_checkin_csv(request):
    """
    Exports filtered data to a CSV file (compatible with Excel).
    """

    # Use the same filter logic to ensure exported data matches the report view's filters
    filter = CheckInFilter(request.GET, queryset=CheckIn.objects.all().order_by('-timestamp'))
    records = filter.qs

    # HTTP Response setup for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PLS_report.csv"'

    writer = csv.writer(response)

    # 1. Write the header row
    writer.writerow([
        'ID',
        'Company',
        'Location',
        'Employee ID',
        'Employee Name',
        'Latitude',
        'Longitude',
        'Timestamp'
    ])

    # 2. Write data rows
    for record in records:
        writer.writerow([
            record.id,
            record.company.name if record.company else 'N/A',
            record.current_location.name if record.current_location else 'N/A',
            record.employee_id,
            record.employee_name,
            record.location_lat,
            record.location_lon,
            record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response