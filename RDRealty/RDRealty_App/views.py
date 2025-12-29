from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count 
from django.db.models.functions import TruncMonth 
from datetime import date, datetime, time
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import json
import os
from pathlib import Path
from urllib.request import urlopen
from django.conf import settings
from django.utils import timezone
import zipfile

from .models import Property, LocalInformation, OwnerInformation, FinancialInformation, AdditionalInformation, SupportingDocument, UserProfile, Notification, PropertyTax
from .forms import PropertyCreateForm


# --- 0. DASHBOARD VIEW (Landing Page) ---
class DashboardView(TemplateView):
    """
    Renders the main dashboard template and provides key metrics.
    Tax and Movement metrics are removed as those models no longer exist.
    """
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- 1. PROPERTY METRICS (TOTAL COUNT) ---
        context['total_properties'] = Property.objects.count()
        
        # -----------------------------------------------------------------
        # --- 2. MONTHLY ADDITIONS LOGIC (UPDATED) ---
        # Using filter with date range for better reliability with timezones
        # -----------------------------------------------------------------
        current_date = timezone.localdate()
        
        # Calculate start of current month
        start_date = current_date.replace(day=1)
        
        # Calculate start of next month
        if start_date.month == 12:
            next_month_date = date(start_date.year + 1, 1, 1)
        else:
            next_month_date = date(start_date.year, start_date.month + 1, 1)
            
        # Convert to aware datetimes for database query
        start_dt = timezone.make_aware(datetime.combine(start_date, time.min))
        end_dt = timezone.make_aware(datetime.combine(next_month_date, time.min))

        # Filter properties added in the current month range
        current_month_count = Property.objects.filter(
            date_added__gte=start_dt,
            date_added__lt=end_dt
        ).count()
        
        context['current_month_added'] = current_month_count
        
        # -----------------------------------------------------------------
        # --- 3. TAX & MOVEMENT METRICS (REMOVED/SET TO DEFAULT) ---
        # These are set to 0.00/0 to prevent errors if dashboard.html still references them.
        # -----------------------------------------------------------------
        context['total_tax_due'] = 0.00
        context['total_tax_paid'] = 0.00
        context['pending_tax_count'] = 0
        context['total_movements'] = 0
        
        # --- 4. OTHER METRICS ---
        context['classification_data'] = []
        context['pending_approvals'] = 0 
        
        return context

# --- 1. PROPERTY CREATION VIEW (KEPT) ---
class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'add_property/property_create.html'
    success_url = reverse_lazy('property_list')
    
    def form_valid(self, form):
        # Handle file uploads validation BEFORE saving anything
        files = self.request.FILES.getlist('ai_supp_docs')
        MAX_FILES = 5
        MAX_SIZE_MB = 10
        MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

        if len(files) > MAX_FILES:
            form.add_error(None, f"You can only upload a maximum of {MAX_FILES} files.")
            return self.form_invalid(form)

        for f in files:
            if f.size > MAX_SIZE_BYTES:
                form.add_error(None, f"File {f.name} exceeds the {MAX_SIZE_MB}MB limit.")
                return self.form_invalid(form)

        response = super().form_valid(form)
        loc_specific = self.request.POST.get('loc_specific', '')
        loc_province = self.request.POST.get('loc_province', '')
        loc_city = self.request.POST.get('loc_city', '')
        loc_barangay = self.request.POST.get('loc_barangay', '')
        LocalInformation.objects.create(
            property_id=self.object.property_id,
            loc_specific=loc_specific,
            loc_province=loc_province,
            loc_city=loc_city,
            loc_barangay=loc_barangay
        )

        oi_fullname = self.request.POST.get('oi_fullname', '')
        oi_bankname = self.request.POST.get('oi_bankname', '')
        oi_custody_title = self.request.POST.get('oi_custody_title', '')
        OwnerInformation.objects.create(
            property_id=self.object.property_id,
            oi_fullname=oi_fullname,
            oi_bankname=oi_bankname,
            oi_custody_title=oi_custody_title
        )

        fi_encumbrance = self.request.POST.get('fi_encumbrance', '')
        fi_mortgage = self.request.POST.get('fi_mortgage', '')
        fi_borrower = self.request.POST.get('fi_borrower', '')
        FinancialInformation.objects.create(
            property_id=self.object.property_id,
            fi_encumbrance=fi_encumbrance,
            fi_mortgage=fi_mortgage,
            fi_borrower=fi_borrower
        )

        ai_remarks = self.request.POST.get('ai_remarks', '')
        AdditionalInformation.objects.create(
            property_id=self.object.property_id,
            ai_remarks=ai_remarks
        )

        # Save files after successful form validation
        for f in files:
            SupportingDocument.objects.create(
                property_id=self.object.property_id,
                file=f
            )

        Notification.objects.create(
            category='PROPERTY',
            message=f"New Property added with Title No.: {self.object.title_no}"
        )

        return response

# --- 1.5 PROPERTY UPDATE VIEW ---
class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'add_property/property_update.html'
    success_url = reverse_lazy('property_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            return redirect('property_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Try to get existing local info
        try:
            local_info = LocalInformation.objects.get(property_id=self.object.property_id)
            context['local_info'] = local_info
        except LocalInformation.DoesNotExist:
            context['local_info'] = None

        # Try to get existing owner info
        try:
            owner_info = OwnerInformation.objects.get(property_id=self.object.property_id)
            context['owner_info'] = owner_info
        except OwnerInformation.DoesNotExist:
            context['owner_info'] = None

        # Try to get existing financial info
        try:
            financial_info = FinancialInformation.objects.get(property_id=self.object.property_id)
            context['financial_info'] = financial_info
        except FinancialInformation.DoesNotExist:
            context['financial_info'] = None

        # Try to get existing additional info
        try:
            additional_info = AdditionalInformation.objects.get(property_id=self.object.property_id)
            context['additional_info'] = additional_info
        except AdditionalInformation.DoesNotExist:
            context['additional_info'] = None

        # Get existing supporting documents
        context['supporting_docs'] = SupportingDocument.objects.filter(property_id=self.object.property_id)

        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('ai_supp_docs')
        delete_ids = self.request.POST.getlist('delete_files')
        
        current_docs = SupportingDocument.objects.filter(property_id=self.object.property_id)
        current_count = current_docs.count()
        
        valid_delete_ids = list(current_docs.filter(id__in=delete_ids).values_list('id', flat=True))
        
        projected_count = current_count - len(valid_delete_ids) + len(files)
        
        MAX_FILES = 5
        MAX_SIZE_MB = 10
        MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

        if projected_count > MAX_FILES:
             form.add_error(None, f"Total files cannot exceed {MAX_FILES}. You currently have {current_count}, are deleting {len(valid_delete_ids)}, and adding {len(files)}.")
             return self.form_invalid(form)

        for f in files:
            if f.size > MAX_SIZE_BYTES:
                form.add_error(None, f"File {f.name} exceeds the {MAX_SIZE_MB}MB limit.")
                return self.form_invalid(form)

        docs_to_delete = []
        if valid_delete_ids:
            docs_to_delete = list(SupportingDocument.objects.filter(id__in=valid_delete_ids))
            deleted_root = Path(settings.MEDIA_ROOT) / "supporting_docs" / "Deleted_Files"
            deleted_root.mkdir(parents=True, exist_ok=True)
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            zip_name = f"deleted_{self.object.property_id}_{timestamp}.zip"
            zip_path = deleted_root / zip_name
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for doc in docs_to_delete:
                    try:
                        file_path = Path(doc.file.path)
                    except (ValueError, AttributeError):
                        continue
                    if file_path.is_file():
                        archive.write(str(file_path), arcname=file_path.name)
                        try:
                            file_path.unlink()
                        except OSError:
                            pass
            SupportingDocument.objects.filter(id__in=valid_delete_ids).delete()

        response = super().form_valid(form)
        loc_specific = self.request.POST.get('loc_specific', '')
        loc_province = self.request.POST.get('loc_province', '')
        loc_city = self.request.POST.get('loc_city', '')
        loc_barangay = self.request.POST.get('loc_barangay', '')
        
        # Update or create
        LocalInformation.objects.update_or_create(
            property_id=self.object.property_id,
            defaults={
                'loc_specific': loc_specific,
                'loc_province': loc_province,
                'loc_city': loc_city,
                'loc_barangay': loc_barangay
            }
        )

        oi_fullname = self.request.POST.get('oi_fullname', '')
        oi_bankname = self.request.POST.get('oi_bankname', '')
        oi_custody_title = self.request.POST.get('oi_custody_title', '')

        OwnerInformation.objects.update_or_create(
            property_id=self.object.property_id,
            defaults={
                'oi_fullname': oi_fullname,
                'oi_bankname': oi_bankname,
                'oi_custody_title': oi_custody_title
            }
        )

        fi_encumbrance = self.request.POST.get('fi_encumbrance', '')
        fi_mortgage = self.request.POST.get('fi_mortgage', '')
        fi_borrower = self.request.POST.get('fi_borrower', '')

        FinancialInformation.objects.update_or_create(
            property_id=self.object.property_id,
            defaults={
                'fi_encumbrance': fi_encumbrance,
                'fi_mortgage': fi_mortgage,
                'fi_borrower': fi_borrower
            }
        )

        ai_remarks = self.request.POST.get('ai_remarks', '')
        AdditionalInformation.objects.update_or_create(
            property_id=self.object.property_id,
            defaults={
                'ai_remarks': ai_remarks
            }
        )

        # Handle file uploads (append new files)
        for f in files:
            SupportingDocument.objects.create(
                property_id=self.object.property_id,
                file=f
            )

        Notification.objects.create(
            category='PROPERTY',
            message=f"Property updated with Title No.: {self.object.title_no}"
        )

        return response

# --- 2. PROPERTY LIST VIEW (KEPT) ---
class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'
    context_object_name = 'properties'
    ordering = ['title_no']
    paginate_by = 20  # Add pagination

    def get_queryset(self):
        # Optimize: Prefetch related data to avoid N+1 queries
        queryset = Property.objects.prefetch_related('ownerinformation_set').all()
        
        q = self.request.GET.get('q')
        if q:
            class_matches = [k for k, v in Property.CLASSIFICATION_CHOICES if q.lower() in v.lower()]
            status_matches = [k for k, v in Property.STATUS_CHOICES if q.lower() in v.lower()]
            
            query = Q(title_no__icontains=q) | \
                    Q(lot_no__icontains=q) | \
                    Q(title_description__icontains=q) | \
                    Q(lot_area__icontains=q) | \
                    Q(property_id__icontains=q) | \
                    Q(date_added__icontains=q) | \
                    Q(localinformation__loc_province__icontains=q) | \
                    Q(localinformation__loc_city__icontains=q) | \
                    Q(localinformation__loc_barangay__icontains=q) | \
                    Q(localinformation__loc_specific__icontains=q) | \
                    Q(ownerinformation__oi_fullname__icontains=q) | \
                    Q(ownerinformation__oi_bankname__icontains=q) | \
                    Q(ownerinformation__oi_custody_title__icontains=q) | \
                    Q(financialinformation__fi_encumbrance__icontains=q) | \
                    Q(financialinformation__fi_mortgage__icontains=q) | \
                    Q(financialinformation__fi_borrower__icontains=q) | \
                    Q(additionalinformation__ai_remarks__icontains=q) | \
                    Q(supportingdocument__file__icontains=q)
            
            if class_matches:
                query |= Q(title_classification__in=class_matches)
            query |= Q(title_classification__icontains=q)
            
            if status_matches:
                query |= Q(title_status__in=status_matches)
            query |= Q(title_status__icontains=q)
            
            queryset = queryset.filter(query).distinct()
            
        # Classification filter (Dropdown)
        classification = self.request.GET.get('classification')
        if classification and classification != 'Classification':
            queryset = queryset.filter(title_classification=classification)
            
        # Status filter (Dropdown)
        status = self.request.GET.get('status')
        if status and status != 'Status':
            queryset = queryset.filter(title_status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass current filter values to context to maintain state in UI
        context['current_q'] = self.request.GET.get('q', '')
        context['current_classification'] = self.request.GET.get('classification', 'Classification')
        context['current_status'] = self.request.GET.get('status', 'Status')
        context['total_properties_count'] = Property.objects.count()
        return context

# --- 3. PROPERTY DETAIL VIEW (UPDATED) ---
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related LocalInformation
        context['local_info'] = self.object.localinformation_set.first()
        # Fetch related OwnerInformation
        context['owner_info'] = self.object.ownerinformation_set.first()
        # Fetch related FinancialInformation
        context['financial_info'] = self.object.financialinformation_set.first()
        # Fetch related AdditionalInformation
        context['additional_info'] = self.object.additionalinformation_set.first()
        # Fetch related SupportingDocuments
        context['supporting_docs'] = self.object.supportingdocument_set.all()
        # Fetch related Tax Records
        context['tax_records'] = self.object.propertytax_set.all().order_by('-tax_year', '-tax_due_date')
        return context

# --- 3.5 ADD PROPERTY TAX API ---
@login_required
def add_property_tax(request, pk):
    if request.method == 'POST':
        try:
            property_obj = get_object_or_404(Property, pk=pk)
            data = json.loads(request.body)
            
            tax_record = PropertyTax.objects.create(
                property=property_obj,
                tax_year=data.get('tax_year'),
                tax_quarter=data.get('tax_quarter'),
                tax_amount=data.get('tax_amount'),
                tax_due_date=data.get('tax_due_date'),
                tax_from=data.get('tax_from'),
                tax_to=data.get('tax_to'),
                tax_status=data.get('tax_status'),
                tax_remarks=data.get('tax_remarks')
            )
            
            Notification.objects.create(
                category='TAX',
                message=f"New Tax Record added for Property: {property_obj.title_no}"
            )

            return JsonResponse({'success': True, 'message': 'Tax record added successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def update_property_tax(request, pk):
    if request.method == 'POST':
        try:
            tax_record = get_object_or_404(PropertyTax, pk=pk)
            data = json.loads(request.body)
            
            tax_record.tax_year = data.get('tax_year')
            tax_record.tax_quarter = data.get('tax_quarter')
            tax_record.tax_amount = data.get('tax_amount')
            tax_record.tax_due_date = data.get('tax_due_date')
            tax_record.tax_from = data.get('tax_from')
            tax_record.tax_to = data.get('tax_to')
            tax_record.tax_status = data.get('tax_status')
            tax_record.tax_remarks = data.get('tax_remarks')
            
            tax_record.save()
            
            return JsonResponse({'success': True, 'message': 'Tax record updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

# --- 4. GLOBAL SEARCH API ---
def global_search(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        properties = Property.objects.prefetch_related('ownerinformation_set', 'localinformation_set').filter(
            Q(title_no__icontains=query) | 
            Q(lot_no__icontains=query) |
            Q(title_classification__icontains=query) |
            Q(title_status__icontains=query) |
            Q(title_description__icontains=query) |
            Q(property_id__icontains=query) |
            Q(lot_area__icontains=query) |
            Q(localinformation__loc_province__icontains=query) |
            Q(localinformation__loc_city__icontains=query) |
            Q(localinformation__loc_barangay__icontains=query) |
            Q(localinformation__loc_specific__icontains=query) |
            Q(ownerinformation__oi_fullname__icontains=query) |
            Q(ownerinformation__oi_bankname__icontains=query) |
            Q(ownerinformation__oi_custody_title__icontains=query) |
            Q(financialinformation__fi_encumbrance__icontains=query) |
            Q(financialinformation__fi_mortgage__icontains=query) |
            Q(financialinformation__fi_borrower__icontains=query) |
            Q(additionalinformation__ai_remarks__icontains=query) |
            Q(supportingdocument__file__icontains=query)
        ).distinct()[:5]
        
        for prop in properties:
            owner = prop.ownerinformation_set.first()
            owner_name = owner.oi_fullname if owner and owner.oi_fullname else ""
            loc = prop.localinformation_set.first()
            loc_parts = []
            if loc and loc.loc_barangay:
                loc_parts.append(loc.loc_barangay)
            if loc and loc.loc_city:
                loc_parts.append(loc.loc_city)
            if loc and loc.loc_province:
                loc_parts.append(loc.loc_province)
            loc_text = ", ".join(loc_parts) if loc_parts else ""

            results.append({
                'category': 'Property',
                'title': prop.title_no,
                'description': f"{owner_name or 'No owner'} | Lot {prop.lot_no} | {loc_text or prop.get_title_classification_display()}",
                'url': str(reverse_lazy('property_detail', kwargs={'pk': prop.pk}))
            })

        # Search User Management
        # Include Profile full_name in search
        users = User.objects.select_related('profile').filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__full_name__icontains=query)
        )[:5]

        for user in users:
            role = "Admin" if user.is_staff else "User"
            status = "Active" if user.is_active else "Inactive"
            # Try to get full name from profile, fallback to first/last or username
            full_name = user.username
            if hasattr(user, 'profile') and user.profile.full_name:
                full_name = user.profile.full_name
            
            results.append({
                'category': 'User Management',
                'title': full_name, # Show Fullname as main title as requested
                'description': f"{user.username} | {role} | {status}",
                # Use update URL if user is admin, else maybe list? Using update for now as it's the "detail" view
                'url': str(reverse_lazy('user_view', kwargs={'user_id': user.id}))
            })

        # Tax Record Search
        taxes = PropertyTax.objects.select_related('property').filter(
            Q(id__icontains=query) |
            Q(tax_year__icontains=query) |
            Q(tax_quarter__icontains=query) |
            Q(tax_amount__icontains=query) |
            Q(tax_due_date__icontains=query) |
            Q(tax_status__icontains=query) |
            Q(property__title_no__icontains=query) |
            Q(property__lot_no__icontains=query)
        )[:5]

        for tax in taxes:
            results.append({
                'category': 'Tax Record',
                'title': f"Receipt {tax.id}",
                'description': f"{tax.property.title_no} | Lot {tax.property.lot_no} | {tax.tax_year} | {tax.tax_status}",
                'url': str(reverse_lazy('property_detail', kwargs={'pk': tax.property.pk}))
            })
            
    return JsonResponse({'results': results})


@login_required
def notifications_api(request):
    notifications_qs = Notification.objects.filter(
        created_at__gte=request.user.date_joined
    )

    if not (request.user.is_staff or request.user.is_superuser):
        notifications_qs = notifications_qs.filter(category__in=['PROPERTY', 'TAX'])

    notifications = notifications_qs.order_by('-created_at')[:15]
    data = []
    for n in notifications:
        url = ''
        if n.category == 'PROPERTY':
            marker = 'Title No.:'
            if marker in n.message:
                title_no = n.message.split(marker, 1)[1].strip()
                if title_no:
                    prop = Property.objects.filter(title_no=title_no).first()
                    if prop:
                        url = str(reverse_lazy('property_detail', kwargs={'pk': prop.pk}))
        elif n.category == 'USER':
            if ':' in n.message:
                username = n.message.split(':', 1)[1].strip()
                if username:
                    user = User.objects.filter(username=username).first()
                    if user:
                        url = str(reverse_lazy('user_view', kwargs={'user_id': user.id}))
        elif n.category == 'TAX':
            if 'Property:' in n.message:
                title_no = n.message.split('Property:', 1)[1].strip()
                if title_no:
                    prop = Property.objects.filter(title_no=title_no).first()
                    if prop:
                        url = str(reverse_lazy('property_detail', kwargs={'pk': prop.pk}))

        data.append({
            'id': n.id,
            'category': n.category,
            'message': n.message,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
            'url': url,
        })
    return JsonResponse({'notifications': data})

# --- 5. AUTH: LOGIN VIEW ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        return render(request, 'registration/login.html', {'form': {}, 'error_message': "Invalid username or password."})
    return render(request, 'registration/login.html', {'form': {}})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# --- 7. PH LOCATIONS API (Local JSON) ---
LOCATIONS_DATA = None

def load_locations_data():
    global LOCATIONS_DATA
    if LOCATIONS_DATA is None:
        try:
            file_path = os.path.join(settings.BASE_DIR, 'RDRealty_App', 'static', 'data', 'ph_location.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                LOCATIONS_DATA = json.load(f)
        except Exception as e:
            print(f"Error loading locations data: {e}")
            LOCATIONS_DATA = {"provinces": []}
    return LOCATIONS_DATA

def get_provinces(request):
    try:
        data = load_locations_data()
        # Return provinces without nested cities to keep payload small
        provinces = [{k: v for k, v in p.items() if k != 'cities'} for p in data.get('provinces', [])]
        return JsonResponse(provinces, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_cities(request, province_code):
    try:
        data = load_locations_data()
        # Find the province
        province = next((p for p in data.get('provinces', []) if p['code'] == province_code), None)
        
        if province:
            # Return cities without nested barangays
            cities = [{k: v for k, v in c.items() if k != 'barangays'} for c in province.get('cities', [])]
            return JsonResponse(cities, safe=False)
        else:
            return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_barangays(request, city_code):
    try:
        data = load_locations_data()
        # We need to find the city. Iterate provinces then cities.
        # This might be slightly slow but acceptable for in-memory data.
        # Optimization: could build a map, but let's keep it simple first.
        
        for p in data.get('provinces', []):
            for c in p.get('cities', []):
                if c['code'] == city_code:
                    return JsonResponse(c.get('barangays', []), safe=False)
        
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
# --- 6. USER MANAGEMENT (CRUD) ---
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def user_list(request):
    users = User.objects.all().select_related('profile').order_by('username')
    return render(request, 'user_list.html', {'users': users, 'can_manage': is_admin(request.user)})

@login_required
def user_create(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', 'USER')
        if not username or not full_name or not password1 or password1 != password2:
            return render(request, 'user_form.html', {'error_message': 'Invalid data or passwords do not match.', 'mode': 'create'})
        if User.objects.filter(username=username).exists():
            return render(request, 'user_form.html', {'error_message': 'Username already exists.', 'mode': 'create'})
        u = User.objects.create_user(username=username, password=password1)
        UserProfile.objects.create(user=u, full_name=full_name)
        if role == 'ADMIN' and is_admin(request.user):
            u.is_staff = True
        else:
            u.is_staff = False
        u.save()
        Notification.objects.create(
            category='USER',
            message=f"New user added: {u.username}"
        )
        return redirect('user_list')
    return render(request, 'user_form.html', {'mode': 'create'})

@login_required
def user_update(request, user_id):
    target = User.objects.get(id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=target, defaults={'full_name': target.username})
    if not is_admin(request.user):
        return render(request, 'user_form.html', {'error_message': 'Insufficient permissions.', 'mode': 'update', 'target': target, 'profile': profile})
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        role = request.POST.get('role', 'USER')
        status = request.POST.get('status', 'ACT')
        if username:
            target.username = username
        if full_name:
            profile.full_name = full_name
        target.is_staff = (role == 'ADMIN')
        target.is_active = (status == 'ACT')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1:
            if password1 != password2:
                return render(request, 'user_form.html', {'error_message': 'Passwords do not match.', 'mode': 'update', 'target': target, 'profile': profile})
            target.set_password(password1)
        target.save()
        profile.save()
        Notification.objects.create(
            category='USER',
            message=f"User updated: {target.username}"
        )
        return redirect('user_list')
    return render(request, 'user_form.html', {'mode': 'update', 'target': target, 'profile': profile})

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    target = User.objects.get(id=user_id)
    if request.method == 'POST':
        username = target.username
        target.delete()
        Notification.objects.create(
            category='USER',
            message=f"User deleted: {username}"
        )
        return redirect('user_list')
    return render(request, 'user_form.html', {'mode': 'delete', 'target': target})

@login_required
@user_passes_test(is_admin)
def user_view(request, user_id):
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
            
        # Validate file type (image)
        if not file.content_type.startswith('image/'):
            return JsonResponse({'error': 'Only image files are allowed.'}, status=400)
            
        SupportingDocument.objects.create(
            property_id=property_obj.property_id,
            file=file
        )
        
        Notification.objects.create(
            category='PROPERTY',
            message=f"New document uploaded for Property: {property_obj.title_no}"
        )
        
        return JsonResponse({'success': True, 'message': 'Document uploaded successfully.'})
        
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
