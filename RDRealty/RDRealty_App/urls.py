from django.urls import path
from .views import (
    DashboardView, PropertyCreateView, PropertyListView, PropertyDetailView, PropertyUpdateView,
    global_search, login_view, logout_view, user_list, user_create, user_update, user_delete,
    get_provinces, get_cities, get_barangays
)

urlpatterns = [
    # Landing page: Login
    path('', login_view, name='login'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='app_logout'),
    
    # Dashboard on a separate route
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    
    # 2. Add Property View
    path('add-property/', PropertyCreateView.as_view(), name='add_property'),
    
    # 2.5 Update Property View
    path('property/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_update'),

    # 3. Property Detail View
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    
    # 4. Property List View: This is now moved to a new path to free up the root ('')
    path('properties/', PropertyListView.as_view(), name='property_list'), 
    
    # 5. Global Search API
    path('api/search/', global_search, name='global_search'),
    
    # Locations API (Proxied)
    path('api/locations/provinces/', get_provinces, name='get_provinces'),
    path('api/locations/cities/<str:province_code>/', get_cities, name='get_cities'),
    path('api/locations/barangays/<str:city_code>/', get_barangays, name='get_barangays'),
    
    # 6. User Management
    path('user-management/', user_list, name='user_list'),
    path('user-management/add/', user_create, name='user_create'),
    path('user-management/<int:user_id>/edit/', user_update, name='user_update'),
    path('user-management/<int:user_id>/delete/', user_delete, name='user_delete'),
]
