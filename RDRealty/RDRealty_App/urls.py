from django.urls import path
# ⚠️ FIX: You MUST import the ApprovalsView here, otherwise Django can't find it.
from .views import DashboardView, PropertyCreateView, PropertyListView, PropertyDetailView 

urlpatterns = [
    # 1. NEW ROOT OF THE APP/SITE: This is the Dashboard landing page
    path('', DashboardView.as_view(), name='dashboard'), 
    
    # 2. Add Property View
    path('add-property/', PropertyCreateView.as_view(), name='add_property'),
    
    # 3. Property Detail View
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    
    # 4. Property List View: This is now moved to a new path to free up the root ('')
    path('properties/', PropertyListView.as_view(), name='property_list'), 
    
]