from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
# Import aggregation functions (Removed Sum as TitleMovement and PropertyTax are gone)
from django.db.models import Count 
from django.db.models.functions import TruncMonth 
from datetime import date 

# IMPORTANT: Only import the existing Property model
from .models import Property 
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
        # --- 2. MONTHLY ADDITIONS LOGIC (KEPT) ---
        # -----------------------------------------------------------------
        monthly_data = Property.objects.annotate(
            month_year=TruncMonth('date_added')
        ).values('month_year').annotate(
            count=Count('id')
        ).order_by('-month_year')

        current_month = date.today().replace(day=1)
        current_month_count = 0
        
        for item in monthly_data:
            if item['month_year'].date() == current_month:
                current_month_count = item['count']
                break
        
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

# --- 2. PROPERTY LIST VIEW (KEPT) ---
class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'
    context_object_name = 'properties'
    ordering = ['title_no']

# --- 3. PROPERTY DETAIL VIEW (UPDATED) ---
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Removed lines referencing the related managers for the deleted models
        context['movements'] = [] # Set to empty list placeholder
        context['tax_records'] = [] # Set to empty list placeholder
        return context