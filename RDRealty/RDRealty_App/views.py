from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth 
from datetime import date, datetime, time, timedelta
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import json
import os
from pathlib import Path
from urllib.request import urlopen
from django.conf import settings
from django.utils import timezone
import zipfile

from .models import Property, LocalInformation, OwnerInformation, FinancialInformation, AdditionalInformation, SupportingDocument, UserProfile, Notification, PropertyTax, AIRequestLog, TitleMovementRequest, TitleMovementDocument, PropertyHistory
from .forms import PropertyCreateForm
from .ai_brain import get_ai_response
from django.views.decorators.csrf import csrf_exempt


# --- 0. DASHBOARD VIEW (Landing Page) ---
class DashboardView(TemplateView):
    """
    Renders the main dashboard template and provides key metrics.
    """
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add today's date to context
        context['today'] = timezone.now()
        
        # --- 1. PROPERTY METRICS ---
        context['total_properties'] = Property.objects.count()
        context['active_properties'] = Property.objects.filter(title_status='ACT').count()
        context['collateral_properties'] = Property.objects.filter(title_status='COL').count()
        
        # Monthly additions
        current_date = timezone.localdate()
        start_of_month = timezone.make_aware(datetime.combine(current_date.replace(day=1), time.min))
        context['properties_this_month'] = Property.objects.filter(date_added__gte=start_of_month).count()
        
        # Property Classifications for Chart/List
        classifications = Property.objects.values('title_classification').annotate(count=Count('title_classification'))
        total_count = context['total_properties']
        classification_data = []
        for c in classifications:
            code = c['title_classification']
            name = dict(Property.CLASSIFICATION_CHOICES).get(code, code)
            count = c['count']
            percentage = (count / total_count * 100) if total_count > 0 else 0
            classification_data.append({
                'name': name,
                'count': count,
                'percentage': round(percentage, 1),
                'code': code
            })
        context['classifications'] = classification_data
        
        # --- 2. TAX METRICS ---
        total_paid = PropertyTax.objects.filter(tax_status='Paid').aggregate(total=Sum('tax_amount'))['total'] or 0
        total_due = PropertyTax.objects.exclude(tax_status='Paid').aggregate(total=Sum('tax_amount'))['total'] or 0
        context['total_tax_paid'] = total_paid
        context['total_tax_due'] = total_due
        
        all_tax_sum = PropertyTax.objects.aggregate(total=Sum('tax_amount'))['total'] or 1
        context['collection_rate'] = round((total_paid / all_tax_sum * 100), 1) if all_tax_sum > 0 else 0
        context['overdue_payments'] = PropertyTax.objects.filter(tax_status='Overdue').count()
        
        # Tax Status Breakdown
        tax_statuses = PropertyTax.objects.values('tax_status').annotate(count=Count('tax_status'), total_amount=Sum('tax_amount'))
        context['tax_status_overview'] = tax_statuses

        # --- 3. TITLE MOVEMENT METRICS ---
        context['total_movements'] = TitleMovementRequest.objects.count()
        context['returned_movements'] = TitleMovementRequest.objects.filter(status='Returned').count()
        context['currently_out'] = TitleMovementRequest.objects.exclude(status='Returned').count()
        # Assuming 'Overdue' logic for movements if exists, otherwise 0
        context['overdue_returns'] = 0 
        
        # Movement Status Breakdown
        context['movement_status_overview'] = TitleMovementRequest.objects.values('status').annotate(count=Count('status'))

        # --- 4. RECENTLY ADDED PROPERTIES ---
        context['recent_properties'] = Property.objects.all().prefetch_related('ownerinformation_set').order_by('-date_added')[:5]

        return context

# --- AUTH VIEWS ---
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# --- PROPERTY VIEWS ---
class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'
    context_object_name = 'properties'
    paginate_by = 10

    def get_queryset(self):
        qs = Property.objects.all().order_by('-date_added')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title_no__icontains=q) | 
                Q(lot_no__icontains=q) |
                Q(property_id__icontains=q)
            )
        return qs

class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'add_property/property_create.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        
        # Track initial creation for Property model fields
        fields_to_track = ['title_no', 'lot_no', 'lot_area', 'title_classification', 'title_status', 'title_description']
        for field in fields_to_track:
            val = getattr(self.object, field)
            
            # Map choice codes to labels
            if field == 'title_classification':
                val = dict(Property.CLASSIFICATION_CHOICES).get(val, val)
            elif field == 'title_status':
                val = dict(Property.STATUS_CHOICES).get(val, val)
                
            track_field_change(
                self.object, 
                self.request.user, 
                field.replace('_', ' ').title(), 
                None, 
                val,
                change_type='ADD'
            )
            
        # Save related info with 'ADD' type
        save_related_info(self.object, self.request, change_type='ADD')
        
        Notification.objects.create(
            user=self.request.user,
            category='PROPERTY',
            message=f"New property added: {self.object.title_no}"
        )
        return super().form_valid(form)

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'add_property/property_update.html'
    success_url = reverse_lazy('property_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = 'edit'
        obj = self.object
        context['local_info'] = LocalInformation.objects.filter(property=obj).first()
        context['owner_info'] = OwnerInformation.objects.filter(property=obj).first()
        context['financial_info'] = FinancialInformation.objects.filter(property=obj).first()
        context['additional_info'] = AdditionalInformation.objects.filter(property=obj).first()
        context['supporting_docs'] = SupportingDocument.objects.filter(property_id=obj.property_id)
        return context

    def form_valid(self, form):
        # Store old values before saving
        old_obj = Property.objects.get(pk=self.object.pk)
        
        response = super().form_valid(form)
        
        # Track changes for Property model fields
        fields_to_track = ['title_no', 'lot_no', 'lot_area', 'title_classification', 'title_status', 'title_description']
        for field in fields_to_track:
            old_val = getattr(old_obj, field)
            new_val = getattr(self.object, field)
            
            # Map choice codes to labels for better readability in history
            if field == 'title_classification':
                old_val = dict(Property.CLASSIFICATION_CHOICES).get(old_val, old_val)
                new_val = dict(Property.CLASSIFICATION_CHOICES).get(new_val, new_val)
            elif field == 'title_status':
                old_val = dict(Property.STATUS_CHOICES).get(old_val, old_val)
                new_val = dict(Property.STATUS_CHOICES).get(new_val, new_val)
                
            track_field_change(
                self.object, 
                self.request.user, 
                field.replace('_', ' ').title(), 
                old_val, 
                new_val,
                change_type='STATUS_CHANGE' if field == 'title_status' else 'UPDATE'
            )
            
        # Save related info (this function will also need to track changes)
        save_related_info(self.object, self.request)
        
        Notification.objects.create(
            user=self.request.user,
            category='PROPERTY',
            message=f"Property updated: {self.object.title_no}"
        )
        return response

def track_field_change(property_obj, user, field_name, old_value, new_value, change_type='UPDATE', reason=None):
    """Helper to record changes in PropertyHistory."""
    if old_value is None: old_value = ""
    if new_value is None: new_value = ""
    
    # Convert to string for comparison
    old_value_str = str(old_value).strip()
    new_value_str = str(new_value).strip()
    
    # Only track if value actually changed or if it's an 'ADD' event with a non-empty value
    if change_type == 'ADD':
        if new_value_str:
            PropertyHistory.objects.create(
                property=property_obj,
                change_type=change_type,
                field_name=field_name,
                old_value="",
                new_value=new_value_str,
                reason=reason or "Initial creation",
                changed_by=user
            )
    elif old_value_str != new_value_str:
        PropertyHistory.objects.create(
            property=property_obj,
            change_type=change_type,
            field_name=field_name,
            old_value=old_value_str,
            new_value=new_value_str,
            reason=reason,
            changed_by=user
        )

def save_related_info(property_obj, request, change_type='UPDATE'):
    """
    Helper function to save related information for a property.
    """
    # 1. Local Information
    local_info, _ = LocalInformation.objects.get_or_create(property=property_obj)
    
    # Track Local Info changes
    loc_fields = {
        'loc_specific': 'Location Specific',
        'loc_province': 'Province',
        'loc_city': 'City',
        'loc_barangay': 'Barangay'
    }
    for field, label in loc_fields.items():
        old_val = getattr(local_info, field)
        new_val = request.POST.get(field)
        track_field_change(property_obj, request.user, label, old_val, new_val, change_type=change_type)
        setattr(local_info, field, new_val)
    local_info.save()

    # 2. Owner Information
    owner_info, _ = OwnerInformation.objects.get_or_create(property=property_obj)
    
    owner_fields = {
        'oi_fullname': 'Owner Full Name',
        'oi_bankname': 'Bank Name',
        'oi_custody_title': 'Custody Of Title'
    }
    for field, label in owner_fields.items():
        old_val = getattr(owner_info, field)
        new_val = request.POST.get(field)
        track_field_change(property_obj, request.user, label, old_val, new_val, change_type=change_type)
        setattr(owner_info, field, new_val)
    owner_info.save()

    # 3. Financial Information
    financial_info, _ = FinancialInformation.objects.get_or_create(property=property_obj)
    
    fin_fields = {
        'fi_encumbrance': 'Encumbrance',
        'fi_mortgage': 'Mortgage',
        'fi_borrower': 'Borrower'
    }
    for field, label in fin_fields.items():
        old_val = getattr(financial_info, field)
        new_val = request.POST.get(field)
        track_field_change(property_obj, request.user, label, old_val, new_val, change_type=change_type)
        setattr(financial_info, field, new_val)
    financial_info.save()

    # 4. Additional Information
    additional_info, _ = AdditionalInformation.objects.get_or_create(property=property_obj)
    
    old_remarks = additional_info.ai_remarks
    new_remarks = request.POST.get('ai_remarks')
    track_field_change(property_obj, request.user, 'Remarks', old_remarks, new_remarks, change_type=change_type)
    additional_info.ai_remarks = new_remarks
    additional_info.save()

    # 5. Supporting Documents (Uploads)
    files = request.FILES.getlist('ai_supp_docs')
    for f in files:
        SupportingDocument.objects.create(property=property_obj, file=f)

    # 6. Delete Supporting Documents if requested
    delete_ids = request.POST.getlist('delete_files')
    if delete_ids:
        # Get documents to be deleted
        docs_to_delete = SupportingDocument.objects.filter(id__in=delete_ids, property=property_obj)
        
        # Create Deleted_Files directory if it doesn't exist
        deleted_files_dir = os.path.join(settings.MEDIA_ROOT, 'supporting_docs', 'Deleted_Files')
        os.makedirs(deleted_files_dir, exist_ok=True)
        
        # Create a zip file for the deleted documents
        zip_filename = f"deleted_docs_{property_obj.property_id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(deleted_files_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for doc in docs_to_delete:
                if doc.file and os.path.exists(doc.file.path):
                    # Add file to zip archive
                    zipf.write(doc.file.path, os.path.basename(doc.file.path))
        
        # Delete the original files from filesystem and record in change history
        deleted_file_names = []
        for doc in docs_to_delete:
            if doc.file and os.path.exists(doc.file.path):
                # Record file deletion in change history
                deleted_file_names.append(os.path.basename(doc.file.path))
                os.remove(doc.file.path)
        
        # Record file deletions in change history
        if deleted_file_names:
            track_field_change(
                property_obj,
                request.user,
                'Supporting Documents',
                ', '.join(deleted_file_names),
                '',
                change_type='DOCUMENT_DELETE',
                reason=f"Deleted {len(deleted_file_names)} supporting document(s)"
            )
        
        # Delete the documents from database
        docs_to_delete.delete()

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        
        context['local_info'] = LocalInformation.objects.filter(property=obj).first()
        context['owner_info'] = OwnerInformation.objects.filter(property=obj).first()
        context['financial_info'] = FinancialInformation.objects.filter(property=obj).first()
        context['additional_info'] = AdditionalInformation.objects.filter(property=obj).first()
        context['supporting_docs'] = SupportingDocument.objects.filter(property_id=obj.property_id)
        context['tax_records'] = PropertyTax.objects.filter(property=obj).order_by('-tax_year')
        
        # Title Movements (Optimized)
        context['title_movements'] = obj.title_movements.select_related('tm_released_by', 'tm_approved_by').order_by('-created_at')
        
        # Change History
        history_qs = obj.history.select_related('changed_by').all().order_by('-changed_at')
        
        # History Search/Filters
        q = self.request.GET.get('history_q')
        if q:
            history_qs = history_qs.filter(
                Q(field_name__icontains=q) |
                Q(old_value__icontains=q) |
                Q(new_value__icontains=q) |
                Q(reason__icontains=q) |
                Q(change_type__icontains=q) |
                Q(changed_at__icontains=q) |
                Q(changed_by__username__icontains=q) |
                Q(changed_by__first_name__icontains=q) |
                Q(changed_by__last_name__icontains=q) |
                Q(changed_by__email__icontains=q)
            )
            
        h_type = self.request.GET.get('history_type')
        if h_type and h_type != 'All Types':
            history_qs = history_qs.filter(change_type=h_type)
            
        # Paginate change history - 8 records per page
        paginator = Paginator(history_qs, 8)
        history_page = self.request.GET.get('history_page', 1)
        
        try:
            change_history = paginator.page(history_page)
        except (PageNotAnInteger, EmptyPage):
            # If page is not an integer or out of range, deliver first page
            change_history = paginator.page(1)
            
        context['change_history'] = change_history
        
        return context

# --- TAX VIEWS ---
@login_required
def add_property_tax(request, pk):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, pk=pk)
        
        tax_year = request.POST.get('tax_year')
        tax_quarter = request.POST.get('tax_quarter')
        tax_amount = request.POST.get('tax_amount')
        tax_due_date = request.POST.get('tax_due_date')
        tax_from = request.POST.get('tax_from')
        tax_to = request.POST.get('tax_to')
        tax_status = request.POST.get('tax_status')
        tax_remarks = request.POST.get('tax_remarks')
        
        tax = PropertyTax.objects.create(
            property=property_obj,
            tax_year=tax_year,
            tax_quarter=tax_quarter,
            tax_amount=tax_amount,
            tax_due_date=tax_due_date,
            tax_from=tax_from,
            tax_to=tax_to,
            tax_status=tax_status,
            tax_remarks=tax_remarks,
            created_by=request.user
        )
        
        # Track tax record addition in history
        tax_info = f"Year: {tax_year}, Quarter: {tax_quarter}, Amount: {tax_amount}"
        track_field_change(
            property_obj, 
            request.user, 
            "Tax Record", 
            None, 
            tax_info, 
            change_type='ADD',
            reason=f"Added tax record for {tax_year} {tax_quarter}"
        )
        
        Notification.objects.create(
            user=request.user,
            category='TAX',
            message=f"New tax record added for Property: {property_obj.title_no}"
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def update_property_tax(request, pk):
    tax = get_object_or_404(PropertyTax, pk=pk)
    if request.method == 'POST':
        old_status = tax.tax_status
        new_status = request.POST.get('tax_status')
        
        tax.tax_year = request.POST.get('tax_year')
        tax.tax_quarter = request.POST.get('tax_quarter')
        tax.tax_amount = request.POST.get('tax_amount')
        tax.tax_due_date = request.POST.get('tax_due_date')
        tax.tax_from = request.POST.get('tax_from')
        tax.tax_to = request.POST.get('tax_to')
        tax.tax_status = new_status
        tax.tax_remarks = request.POST.get('tax_remarks')
        tax.save()
        
        # Track tax status change
        if old_status != new_status:
            track_field_change(
                tax.property, 
                request.user, 
                f'Tax Status ({tax.tax_year})', 
                old_status, 
                new_status, 
                change_type='TAX_UPDATE',
                reason=f"Tax status for {tax.tax_year} updated to {new_status}"
            )
        
        Notification.objects.create(
            user=request.user,
            category='TAX',
            message=f"Tax record updated for Property: {tax.property.title_no}"
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=405)

class AllTaxRecordsView(ListView):
    model = PropertyTax
    template_name = 'all_tax_records.html'
    context_object_name = 'tax_records'
    paginate_by = 20

    def get_queryset(self):
        qs = PropertyTax.objects.select_related('property').all().order_by('-tax_year', '-tax_due_date')
        
        # Search filter
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(property__title_no__icontains=q) |
                Q(property__property_id__icontains=q)
            )
            
        # Status filter
        status = self.request.GET.get('status')
        if status and status != 'All Status':
            if status == 'Unpaid':
                qs = qs.exclude(tax_status='Paid')
            else:
                qs = qs.filter(tax_status=status)
                
        # Year filter
        year = self.request.GET.get('year')
        if year and year != 'All Years':
            qs = qs.filter(tax_year=year)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_taxes = PropertyTax.objects.all()
        
        # Metrics
        context['total_records'] = all_taxes.count()
        context['total_amount'] = all_taxes.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
        
        paid_taxes = all_taxes.filter(tax_status='Paid')
        context['paid_count'] = paid_taxes.count()
        context['paid_amount'] = paid_taxes.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
        
        unpaid_taxes = all_taxes.exclude(tax_status='Paid')
        context['unpaid_count'] = unpaid_taxes.count()
        context['unpaid_amount'] = unpaid_taxes.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
        
        context['overdue_count'] = all_taxes.filter(tax_status='Overdue').count()
        
        # Filter options
        context['years'] = sorted(list(set(all_taxes.values_list('tax_year', flat=True))), reverse=True)
        context['current_q'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', 'All Status')
        context['current_year'] = self.request.GET.get('year', 'All Years')
        
        return context

from django.urls import reverse

# --- API VIEWS ---
def global_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    
    if q:
        # 1. Search Properties
        props = Property.objects.filter(
            Q(title_no__icontains=q) | 
            Q(lot_no__icontains=q) |
            Q(property_id__icontains=q)
        ).order_by('-date_added')[:5]
        
        for p in props:
            results.append({
                'title': p.title_no,
                'category': 'Property',
                'description': f"Lot {p.lot_no} - {p.get_title_classification_display()}",
                'url': reverse('property_detail', kwargs={'pk': p.pk}),
                'date': p.date_added
            })

        # 2. Search Title Movements
        movements = TitleMovementRequest.objects.filter(
            Q(tm_transmittal_no__icontains=q) |
            Q(tm_purpose__icontains=q) |
            Q(tm_received_by__icontains=q) |
            Q(property__title_no__icontains=q)
        ).select_related('property').order_by('-created_at')[:5]

        for m in movements:
            results.append({
                'title': f"Movement: {m.tm_transmittal_no}",
                'category': 'Movement',
                'description': f"{m.status} - {m.tm_purpose} for {m.property.title_no}",
                'url': reverse('property_detail', kwargs={'pk': m.property.pk}) + '#movements',
                'date': m.created_at
            })

        # 3. Search Tax Records
        taxes = PropertyTax.objects.filter(
            Q(property__title_no__icontains=q) |
            Q(property__property_id__icontains=q) |
            Q(tax_year__icontains=q)
        ).select_related('property').order_by('-created_at')[:5]

        for t in taxes:
            results.append({
                'title': f"Tax: {t.tax_year} Q{t.tax_quarter}",
                'category': 'Tax',
                'description': f"{t.tax_status} - {t.property.title_no} (Amount: {t.tax_amount})",
                'url': reverse('property_detail', kwargs={'pk': t.property.pk}) + '#tax',
                'date': t.created_at
            })

        # Sort combined results by date (newest first)
        results.sort(key=lambda x: x['date'], reverse=True)
    
    # Remove date from final response to avoid serialization issues if needed, 
    # but JsonResponse can handle datetime if we use a custom encoder or just stringify it.
    # Actually, let's just make it a clean list for the frontend.
    final_results = []
    for r in results:
        final_results.append({
            'title': r['title'],
            'category': r['category'],
            'description': r['description'],
            'url': r['url']
        })

    return JsonResponse({'results': final_results})

@login_required
def notifications_api(request):
    """
    Returns all notifications for the current user, with read status.
    Notifications should persist until explicitly cleared by the user.
    """
    # Get all notifications, not just unread ones
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    
    data = []
    for n in notifs:
        # Check if the current user has read this notification
        is_read = n.read_by.filter(id=request.user.id).exists()
        data.append({
            'id': n.id,
            'category': n.category,
            'message': n.message, 
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_read': is_read
        })
    
    return JsonResponse({'notifications': data})

@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notif_ids = data.get('ids', [])
            if notif_ids:
                notifs = Notification.objects.filter(id__in=notif_ids)
                for n in notifs:
                    n.read_by.add(request.user)
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def clear_all_notifications(request):
    """
    Deletes all notifications for the current user when they click "Clear".
    This should completely remove notifications from the system.
    """
    if request.method == 'POST':
        try:
            # Delete all notifications for the current user
            Notification.objects.filter(user=request.user).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

import requests
import json
import os
from django.conf import settings
from django.core.cache import cache

LOCATION_FILE_PATH = os.path.join(settings.BASE_DIR, 'RDRealty_App', 'static', 'data', 'ph_location.json')

def get_location_data():
    """Helper to get location data from local JSON file or cache."""
    cache_key = 'local_ph_location_data_v2'
    data = cache.get(cache_key)
    
    if data is None:
        if os.path.exists(LOCATION_FILE_PATH):
            try:
                with open(LOCATION_FILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cache.set(cache_key, data, 2592000)  # Cache for 30 days
            except Exception as e:
                print(f"Error reading location file: {e}")
                data = {"provinces": []}
        else:
            data = {"provinces": []}
    return data

def get_provinces(request):
    """
    Fetch provinces from local JSON file for speed and sort them alphabetically.
    """
    data = get_location_data()
    provinces = []
    for p in data.get('provinces', []):
        provinces.append({
            'code': p.get('code'),
            'name': p.get('name')
        })
    # Sort by name ascending
    provinces.sort(key=lambda x: x['name'])
    return JsonResponse(provinces, safe=False)

def get_cities(request, province_code):
    """
    Fetch cities for a province from local JSON file and sort them alphabetically.
    """
    data = get_location_data()
    cities = []
    for p in data.get('provinces', []):
        if str(p.get('code')) == str(province_code):
            for c in p.get('cities', []):
                cities.append({
                    'code': c.get('code'),
                    'name': c.get('name')
                })
            break
    # Sort by name ascending
    cities.sort(key=lambda x: x['name'])
    return JsonResponse(cities, safe=False)

def get_barangays(request, city_code):
    """
    Fetch barangays for a city from local JSON file and sort them alphabetically.
    """
    data = get_location_data()
    barangays = []
    for p in data.get('provinces', []):
        for c in p.get('cities', []):
            if str(c.get('code')) == str(city_code):
                for b in c.get('barangays', []):
                    barangays.append({
                        'code': b.get('code'),
                        'name': b.get('name')
                    })
                # Sort by name ascending
                barangays.sort(key=lambda x: x['name'])
                return JsonResponse(barangays, safe=False)
    return JsonResponse(barangays, safe=False)

# --- USER MANAGEMENT ---
def is_admin(user):
    return user.is_superuser

def is_regular_user(user):
    return not user.is_superuser and user.is_authenticated

def check_admin_permission(user):
    """Check if user is admin, otherwise raise PermissionDenied"""
    if not user.is_superuser:
        raise PermissionDenied("Only administrators can access user management.")

@login_required
def user_list(request):
    check_admin_permission(request.user)
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def user_create(request):
    check_admin_permission(request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'user_form.html', {'error_message': 'Username already exists.'})
        
        # Check if passwords match
        if password1 != password2:
            return render(request, 'user_form.html', {'error_message': 'Passwords do not match.'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Set user role (staff status)
        if role == 'ADMIN':
            user.is_staff = True
            user.save()
        
        # Create user profile with full name
        from .models import UserProfile
        UserProfile.objects.create(user=user, full_name=full_name)
        
        return redirect('user_list')
    return render(request, 'user_form.html')

@login_required
def user_update(request, user_id):
    check_admin_permission(request.user)
    target = get_object_or_404(User, pk=user_id)
    profile = getattr(target, 'profile', None)
    if request.method == 'POST':
        target.username = request.POST.get('username')
        # Only update email if provided, otherwise keep existing value
        email = request.POST.get('email')
        if email:
            target.email = email
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        
        if password1:
            if password1 != password2:
                return render(request, 'user_form.html', {'error_message': 'Passwords do not match.', 'mode': 'update', 'target': target, 'profile': profile})
            target.set_password(password1)
        
        # Update user profile full name
        full_name = request.POST.get('full_name')
        if profile:
            profile.full_name = full_name
            profile.save()
        else:
            # Create profile if it doesn't exist
            from .models import UserProfile
            UserProfile.objects.create(user=target, full_name=full_name)
        
        target.save()
        Notification.objects.create(
            user=request.user,
            category='USER',
            message=f"User updated: {target.username}"
        )
        return redirect('user_list')
    return render(request, 'user_form.html', {'mode': 'update', 'target': target, 'profile': profile})

@login_required
def user_delete(request, user_id):
    check_admin_permission(request.user)
    target = User.objects.get(id=user_id)
    if request.method == 'POST':
        username = target.username
        target.delete()
        Notification.objects.create(
            user=request.user,
            category='USER',
            message=f"User deleted: {username}"
        )
        return redirect('user_list')
    return render(request, 'user_form.html', {'mode': 'delete', 'target': target})

@login_required
def user_view(request, user_id):
    check_admin_permission(request.user)
    target = User.objects.get(id=user_id)
    profile = getattr(target, 'profile', None)
    return render(request, 'user_view.html', {'target': target, 'profile': profile})

@login_required
def upload_document(request, pk):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, pk=pk)
        file = request.FILES.get('document')
        
        if not file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
            
        # Validate file size (10MB)
        MAX_SIZE_MB = 10
        if file.size > MAX_SIZE_MB * 1024 * 1024:
            return JsonResponse({'error': f'File size exceeds {MAX_SIZE_MB}MB limit.'}, status=400)
            
        # Validate file type (images, PDF, Word documents, archives)
        allowed_types = [
            'image/',  # Images
            'application/pdf',  # PDF files
            'application/msword',  # .doc files
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx files
            'application/zip',  # .zip files
            'application/x-rar-compressed',  # .rar files
            'application/vnd.rar'  # Alternative .rar MIME type
        ]
        
        # Also check file extension as fallback (browsers may report different MIME types)
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf', '.doc', '.docx', '.zip', '.rar']
        
        # Debug: Log the detected content type and filename
        print(f"DEBUG: Uploaded file content_type: {file.content_type}")
        print(f"DEBUG: Uploaded file name: {file.name}")
        
        # Check both MIME type and file extension
        mime_type_valid = any(file.content_type.startswith(allowed_type) for allowed_type in allowed_types)
        extension_valid = any(file.name.lower().endswith(ext) for ext in allowed_extensions)
        
        if not (mime_type_valid or extension_valid):
            print(f"DEBUG: File type rejected. Content type: {file.content_type}, Filename: {file.name}")
            return JsonResponse({'error': 'Only image, PDF, Word documents, and archive files (.zip, .rar) are allowed.'}, status=400)
            
        SupportingDocument.objects.create(
            property_id=property_obj.property_id,
            file=file
        )
        
        Notification.objects.create(
            user=request.user,
            category='PROPERTY',
            message=f"New document uploaded for Property: {property_obj.title_no}"
        )
        
        return JsonResponse({'success': True, 'message': 'Document uploaded successfully.'})
        
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def ai_usage_api(request):
    """
    Returns the current usage stats for the AI service.
    This replaces client-side tracking with server-side truth.
    """
    now = timezone.now()
    one_minute_ago = now - timedelta(minutes=1)

    # Count GLOBAL usage (Project Level)
    # Reset at midnight (Local Time)
    now = timezone.now()
    local_now = timezone.localtime(now)
    today_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    # Filter by range to be robust against timezone conversions
    # Filter by USER to ensure individual quotas
    daily_count = AIRequestLog.objects.filter(user=request.user, timestamp__gte=today_start).count()
    minute_count = AIRequestLog.objects.filter(user=request.user, timestamp__gte=one_minute_ago).count()

    return JsonResponse({
        'daily': daily_count,
        'minute': minute_count,
        'daily_limit': 20, # Matches User's Free Tier
        'minute_limit': 5   # Matches User's Free Tier
    })

@login_required
@csrf_exempt
def ai_chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        image_file = request.FILES.get('image', None)
        
        if not user_message and not image_file:
             return JsonResponse({'response': "I need a message or an image to assist you."})
             
        ai_response = get_ai_response(user_message, image_file, user=request.user)
        return JsonResponse({'response': ai_response})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_available_documents(request):
    """
    API endpoint to fetch all available documents for the current user
    """
    # Get all supporting documents that the user has access to
    # For now, return all documents - you might want to filter by user permissions later
    documents = SupportingDocument.objects.all()
    
    document_list = []
    for doc in documents:
        document_list.append({
            'name': doc.file.name.split('/')[-1],  # Get just the filename
            'url': doc.file.url  # Full URL to the document
        })
    
    return JsonResponse({
        'documents': document_list,
        'count': len(document_list)
    })


@login_required
def generate_transmittal_number(request):
    property_id = request.GET.get('property_id')
    
    if property_id:
        # Check if this property already has movement records with transmittal numbers
        existing_movement = TitleMovementRequest.objects.filter(
            property_id=property_id
        ).exclude(tm_transmittal_no='').order_by('-created_at').first()
        
        if existing_movement:
            # Use the existing transmittal number for this property
            transmittal_no = existing_movement.tm_transmittal_no
        else:
            # Generate new sequential number for new property
            year_suffix = datetime.now().strftime('%y')
            prefix = f"TM-{year_suffix}-"
            
            # Find last number for this year
            last_mov = TitleMovementRequest.objects.filter(tm_transmittal_no__startswith=prefix).order_by('tm_transmittal_no').last()
            
            if last_mov:
                try:
                    last_seq = int(last_mov.tm_transmittal_no.split('-')[-1])
                    new_seq = last_seq + 1
                except ValueError:
                    new_seq = 1
            else:
                new_seq = 1
                
            transmittal_no = f"{prefix}{new_seq:05d}"
    else:
        # Fallback: generate sequential number (for backward compatibility)
        year_suffix = datetime.now().strftime('%y')
        prefix = f"TM-{year_suffix}-"
        
        # Find last number for this year
        last_mov = TitleMovementRequest.objects.filter(tm_transmittal_no__startswith=prefix).order_by('tm_transmittal_no').last()
        
        if last_mov:
            try:
                last_seq = int(last_mov.tm_transmittal_no.split('-')[-1])
                new_seq = last_seq + 1
            except ValueError:
                new_seq = 1
        else:
            new_seq = 1
            
        transmittal_no = f"{prefix}{new_seq:05d}"
    
    return JsonResponse({'tm_number': transmittal_no})

@login_required
def add_title_movement(request, pk):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, pk=pk)
        
        tm_purpose = request.POST.get('tm_purpose', '').strip()
        tm_transmittal_no = request.POST.get('tm_transmittal_no', '').strip()
        tm_received_by = request.POST.get('tm_received_by', '').strip()
        
        if not tm_purpose or not tm_transmittal_no or not tm_received_by:
            return JsonResponse({'error': 'All fields are required.'}, status=400)
            
        movement = TitleMovementRequest.objects.create(
            property=property_obj,
            tm_purpose=tm_purpose,
            tm_transmittal_no=tm_transmittal_no,
            tm_received_by=tm_received_by,
            tm_released_by=request.user,
            tm_approved_by=request.user
        )
        
        # Track movement record addition in history
        movement_info = f"Purpose: {tm_purpose}, Transmittal No: {tm_transmittal_no}, Received By: {tm_received_by}"
        track_field_change(
            property_obj, 
            request.user, 
            "Title Movement", 
            None, 
            movement_info, 
            change_type='ADD',
            reason=f"Requested title movement"
        )
        
        # Handle file uploads
        files = request.FILES.getlist('tm_documents')
        MAX_SIZE_MB = 10
        
        for f in files:
            if f.size <= MAX_SIZE_MB * 1024 * 1024:
                TitleMovementDocument.objects.create(
                    movement=movement,
                    file=f
                )
        
        Notification.objects.create(
            user=request.user,
            category='MOVEMENT',
            message=f"Title Movement Requested for Property: {property_obj.title_no}"
        )
        
        return JsonResponse({'success': True, 'message': 'Title Movement requested successfully.'})
        
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


class TitleMovementListView(ListView):
    model = TitleMovementRequest
    template_name = "movements/movement_list.html"
    context_object_name = 'movements'
    paginate_by = 10

    def get_queryset(self):
        qs = TitleMovementRequest.objects.all().select_related(
            'property', 
            'tm_released_by', 
            'tm_approved_by'
        ).prefetch_related('property__ownerinformation_set').order_by('-created_at')
        
        # Search filter
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(tm_transmittal_no__icontains=q) |
                Q(property__title_no__icontains=q) |
                Q(property__property_id__icontains=q)
            )
            
        # Status filter
        status = self.request.GET.get('status')
        if status and status != 'All Status':
            qs = qs.filter(status=status)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Summary Counts
        context['released_count'] = TitleMovementRequest.objects.filter(status='Released').count()
        context['in_transit_count'] = TitleMovementRequest.objects.filter(status='In Transit').count()
        context['received_count'] = TitleMovementRequest.objects.filter(status='Received').count()
        context['returned_count'] = TitleMovementRequest.objects.filter(status='Returned').count()
        context['lost_count'] = TitleMovementRequest.objects.filter(status='Lost').count()
        context['pending_return_count'] = TitleMovementRequest.objects.filter(status='Pending Return').count()
        
        # Filters for template
        context['current_q'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', 'All Status')
        
        return context

class UpdateTitleMovementStatusView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
            
        # Check if user is admin
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Only administrators can update title movements'}, status=403)
            
        movement_id = request.POST.get('movement_id')
        new_status = request.POST.get('new_status')
        transmittal_no = request.POST.get('tm_transmittal_no')
        turned_over_by = request.POST.get('tm_turned_over_by')
        received_by = request.POST.get('tm_received_by')
        returned_by = request.POST.get('tm_returned_by')
        received_by_on_return = request.POST.get('tm_received_by_on_return')
        
        if not movement_id or not new_status:
             return JsonResponse({'success': False, 'error': 'Missing movement_id or new_status'})
        
        try:
            movement = TitleMovementRequest.objects.get(pk=movement_id)
            old_status = movement.status
            movement.status = new_status
            
            # Update returned_at logic if needed
            if new_status == 'Returned':
                 movement.returned_at = timezone.now()
                 if returned_by:
                     movement.tm_returned_by = returned_by
                 if received_by_on_return:
                     movement.tm_received_by_on_return = received_by_on_return
            elif new_status == 'Released':
                 movement.returned_at = None
            elif new_status == 'In Transit':
                 if transmittal_no:
                     movement.tm_transmittal_no = transmittal_no
            elif new_status == 'Received':
                 if turned_over_by:
                     movement.tm_turned_over_by = turned_over_by
                 if received_by:
                     movement.tm_received_by = received_by
            elif new_status == 'Lost':
                 # Any specific logic for lost? For now just set the status
                 pass
            elif new_status == 'Pending Return':
                 # Set returned_at to None if it was previously set, or keep it?
                 # Usually pending return means it's not yet returned.
                 movement.returned_at = None
            
            movement.save()
            
            # Track status change in history
            track_field_change(
                movement.property, 
                request.user, 
                'Movement Status', 
                old_status, 
                new_status, 
                change_type='STATUS_CHANGE',
                reason=f"Title movement updated to {new_status}"
            )
            
            Notification.objects.create(
                user=request.user,
                category='MOVEMENT',
                message=f"Title Movement Status Updated: {movement.tm_transmittal_no} -> {new_status}"
            )
            
            return JsonResponse({'success': True})
        except TitleMovementRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Movement not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

# --- DELETE VIEWS ---
@login_required
@user_passes_test(is_admin)
def property_delete(request, pk):
    """Delete a property and its related information."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title_no = property_obj.title_no
        property_obj.delete()
        Notification.objects.create(
            user=request.user,
            category='PROPERTY',
            message=f"Property deleted: {title_no}"
        )
        return redirect('property_list')
    return redirect('property_detail', pk=pk)

@login_required
@user_passes_test(is_admin)
def tax_record_delete(request, pk):
    """Delete a property tax record."""
    tax = get_object_or_404(PropertyTax, pk=pk)
    if request.method == 'POST':
        property_title = tax.property.title_no
        tax_year = tax.tax_year
        tax.delete()
        Notification.objects.create(
            user=request.user,
            category='TAX',
            message=f"Tax record deleted for {property_title} (Year: {tax_year})"
        )
        return redirect('all_tax_records')
    return redirect('all_tax_records')

@login_required
@user_passes_test(is_admin)
def movement_delete(request, pk):
    """Delete a title movement record."""
    movement = get_object_or_404(TitleMovementRequest, pk=pk)
    if request.method == 'POST':
        transmittal_no = movement.tm_transmittal_no
        movement.delete()
        Notification.objects.create(
            user=request.user,
            category='MOVEMENT',
            message=f"Title Movement deleted: {transmittal_no}"
        )
        return redirect('movement_list')


# --- REPORT VIEWS ---
@login_required
def property_tax_movement_report(request):
    """
    Generate a comprehensive report of properties with tax and movement information
    with filtering capabilities.
    """
    # Get all properties with related data
    properties = Property.objects.all().select_related().prefetch_related(
        'propertytax_set',
        'title_movements',
        'ownerinformation_set'
    )
    
    # Apply filters
    property_status = request.GET.get('property_status')
    tax_status = request.GET.get('tax_status')
    movement_status = request.GET.get('movement_status')
    due_date_from = request.GET.get('due_date_from')
    due_date_to = request.GET.get('due_date_to')
    owner_name = request.GET.get('owner_name')
    
    if property_status:
        properties = properties.filter(title_status=property_status)
    
    # Build report data
    report_data = []
    
    for property in properties:
        # Get owner information
        owner_info = property.ownerinformation_set.first()
        owner_name_val = owner_info.oi_fullname if owner_info else None
        
        # Apply owner name filter
        if owner_name and owner_name_val:
            if owner_name.lower() not in owner_name_val.lower():
                continue
        elif owner_name and not owner_name_val:
            # If filtering by owner name but property has no owner info, skip
            continue
        
        # Get latest tax record
        tax_records = property.propertytax_set.all()
        if tax_status:
            tax_records = tax_records.filter(tax_status=tax_status)
        if due_date_from:
            tax_records = tax_records.filter(tax_due_date__gte=due_date_from)
        if due_date_to:
            tax_records = tax_records.filter(tax_due_date__lte=due_date_to)
        
        latest_tax = tax_records.order_by('-tax_due_date').first()
        
        # Get latest movement
        movements = property.title_movements.all()
        if movement_status:
            movements = movements.filter(status=movement_status)
        
        latest_movement = movements.order_by('-created_at').first()
        
        # Only include properties that match all filters
        if (tax_status and not tax_records.exists()) or (movement_status and not movements.exists()):
            continue
        
        report_data.append({
            'property_id': property.property_id,
            'title_no': property.title_no,
            'lot_no': property.lot_no,
            'owner_name': owner_name_val,
            'property_status': property.title_status,
            'tax_amount': latest_tax.tax_amount if latest_tax else None,
            'tax_status': latest_tax.tax_status if latest_tax else None,
            'due_date': latest_tax.tax_due_date if latest_tax else None,
            'movement_status': latest_movement.status if latest_movement else None,
            'last_movement_date': latest_movement.created_at if latest_movement else None
        })
    
    # Pagination
    paginator = Paginator(report_data, 25)  # Show 25 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Summary counts
    total_properties = Property.objects.count()
    due_taxes_count = PropertyTax.objects.filter(tax_status='Due').count()
    overdue_taxes_count = PropertyTax.objects.filter(tax_status='Overdue').count()
    active_movements_count = TitleMovementRequest.objects.filter(
        Q(status='Released') | Q(status='In Transit') | Q(status='Received')
    ).count()
    
    context = {
        'report_data': page_obj,
        'total_properties': total_properties,
        'due_taxes_count': due_taxes_count,
        'overdue_taxes_count': overdue_taxes_count,
        'active_movements_count': active_movements_count,
    }
    
    return render(request, 'reports/property_tax_movement_report.html', context)


@login_required
def delete_document_with_compression(request, doc_id):
    """
    API endpoint to delete a supporting document with compression and archiving
    """
    try:
        # Get the document
        document = get_object_or_404(SupportingDocument, id=doc_id)
        
        # Check if user has permission to delete this document
        # (For now, allow deletion if user is authenticated)
        
        # Create Deleted_Files directory if it doesn't exist
        deleted_files_dir = os.path.join(settings.MEDIA_ROOT, 'supporting_docs', 'Deleted_Files')
        os.makedirs(deleted_files_dir, exist_ok=True)
        
        # Generate archive filename with timestamp
        timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")
        original_filename = os.path.basename(document.file.name)
        archive_filename = f"deleted_{timestamp}_{original_filename}.zip"
        archive_path = os.path.join(deleted_files_dir, archive_filename)
        
        # Create compressed archive
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the original file to the archive
            zipf.write(document.file.path, original_filename)
            
            # Add metadata file
            metadata = {
                'original_filename': original_filename,
                'deleted_at': timezone.localtime(timezone.now()).isoformat(),
                'deleted_by': request.user.username if request.user.is_authenticated else 'unknown',
                'property_id': document.property.property_id if document.property else 'unknown',
                'original_path': document.file.name,
                'file_size': os.path.getsize(document.file.path)
            }
            
            # Create metadata file content
            metadata_content = '\n'.join([f"{key}: {value}" for key, value in metadata.items()])
            zipf.writestr('deletion_metadata.txt', metadata_content)
        
        # Delete the original file from filesystem
        if os.path.exists(document.file.path):
            os.remove(document.file.path)
        
        # Record the deletion in change history
        if document.property:
            PropertyHistory.objects.create(
                property=document.property,
                field_name='Supporting Document',
                old_value=original_filename,
                new_value='DELETED',
                change_type='DOCUMENT_DELETE',
                reason=f'Document archived to {archive_filename}',
                changed_by=request.user
            )
        
        # Create notification for document deletion
        notification_message = f'Document "{original_filename}" was deleted and archived'
        if document.property:
            notification_message += f' for property {document.property.title_no}'
        
        Notification.objects.create(
            category='DOCUMENT',
            message=notification_message,
            user=request.user
        )
        
        # Delete the database record
        document.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Document archived to {archive_filename}',
            'archive_path': archive_path
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error deleting document: {str(e)}'
        }, status=500)


def handler403(request, exception=None):
    """Custom 403 Forbidden error handler"""
    if isinstance(exception, PermissionDenied):
        message = str(exception)
    else:
        message = "You don't have permission to access this page."
    
    return render(request, '403.html', {'message': message}, status=403)
