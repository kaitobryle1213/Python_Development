from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckIn, Company 
from django.views.decorators.http import require_http_methods
from decimal import Decimal, InvalidOperation
from .forms import CompanyForm, CustomUserCreationForm, UserEditForm # Ensure this Form is defined
from django.http import HttpResponse, HttpResponseForbidden
from .filters import CheckInFilter
import csv
from datetime import datetime
from django.urls import reverse # Required for redirects if not using name directly
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django import forms

# Define the exact format string matching the JavaScript output: 'Dec 03, 2025 15:50'
CLIENT_DATETIME_FORMAT = '%b %d, %Y %H:%M'

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@require_http_methods(["GET", "POST"])
def checkin_view(request):
    """Handles the display and submission of the CheckIn form."""
    error_message = None
    companies = Company.objects.all()
    
    # Auto-fill data from logged-in user
    user = request.user
    # Get Employee ID from profile (safely handle missing profile)
    try:
        user_employee_id = user.userprofile.employee_id
    except Exception: # Catch RelatedObjectDoesNotExist or other errors
        user_employee_id = ''
        
    user_full_name = user.get_full_name()

    if request.method == 'POST':
        # 1. Retrieve data
        # NOTE: employee_name and employee_id are now disabled in the form, so we use the user data directly.
        name = user_full_name
        id_num = user_employee_id
        
        lat_str = request.POST.get('location_lat')
        lon_str = request.POST.get('location_lon')
        selfie = request.FILES.get('selfie_photo')
        company_id = request.POST.get('company_id')
        current_location_id = request.POST.get('current_location_id')

        # NEW: Retrieve the client's timestamp string
        client_timestamp_str = request.POST.get('client_timestamp')

        # 2. Validation (Updated to include current_location_id and client_timestamp_str)
        # Check name/id_num availability in case user profile is incomplete
        if not all([name, id_num, lat_str, lon_str, selfie, company_id, current_location_id, client_timestamp_str]):
            error_message = 'Submission failed: Missing required fields. Please ensure your profile has a Full Name and Employee ID.'
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
                        timestamp=client_dt,  # CRITICAL CHANGE: Use the parsed client time
                        user=request.user # Associate with the logged-in user
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
        'error_message': error_message,
        'auto_employee_id': user_employee_id,
        'auto_employee_name': user_full_name
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
# EXISTING VIEW: COMPANY MANAGEMENT (Restricted to Admin)
# ----------------------------------------------------------------------

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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
# EXISTING VIEW: REPORT & FILTERING (Updated for Access Control)
# ----------------------------------------------------------------------

@login_required
def checkin_report_view(request):
    """
    Displays the CheckIn records and allows filtering.
    """
    # Instantiate the filter using the request GET parameters
    # Optimized query with select_related
    queryset = CheckIn.objects.select_related('company', 'current_location').all().order_by('-timestamp')
    
    # Restrict data for non-admin users
    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    filter = CheckInFilter(request.GET, queryset=queryset)
    
    # Pagination
    paginator = Paginator(filter.qs, 20) # Show 20 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'records': page_obj,  # The filtered queryset results (paginated)
        'is_paginated': True,
        'page_obj': page_obj
    }
    return render(request, 'checkin/checkin_report.html', context)


# ----------------------------------------------------------------------
# EXISTING VIEW: EXPORT TO CSV (EXCEL) (Updated for Access Control)
# ----------------------------------------------------------------------

@login_required
def export_checkin_csv(request):
    """
    Exports filtered data to a CSV file (compatible with Excel).
    """

    # Use the same filter logic to ensure exported data matches the report view's filters
    queryset = CheckIn.objects.select_related('company', 'current_location').all().order_by('-timestamp')
    
    # Restrict data for non-admin users
    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    filter = CheckInFilter(request.GET, queryset=queryset)
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

# ----------------------------------------------------------------------
# ⭐ NEW VIEWS: USER MANAGEMENT
# ----------------------------------------------------------------------



@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    users = User.objects.all().order_by('username')
    return render(request, 'checkin/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'checkin/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
def user_edit_view(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # Permission Check:
    # 1. Admin can edit anyone.
    # 2. Standard user can ONLY edit themselves.
    if not request.user.is_staff and request.user.pk != user_obj.pk:
         return HttpResponseForbidden("You are not allowed to edit this user.")

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj, request_user=request.user)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect('user_list')
            else:
                return redirect('checkin_form')
    else:
        # Initialize is_staff from the user object
        initial_data = {'is_staff': user_obj.is_staff}
        form = UserEditForm(instance=user_obj, initial=initial_data, request_user=request.user)
        
    return render(request, 'checkin/user_form.html', {'form': form, 'title': 'Edit User'})

@login_required
@user_passes_test(is_admin)
def user_delete_view(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        return redirect('user_list')
    return render(request, 'checkin/user_confirm_delete.html', {'user_obj': user_obj})
