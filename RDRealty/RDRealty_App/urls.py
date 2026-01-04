from django.urls import path
from .views import (
    DashboardView, PropertyCreateView, PropertyListView, PropertyDetailView, PropertyUpdateView,
    global_search, notifications_api, mark_notifications_read, clear_all_notifications, logout_view, user_list, user_create, user_update, user_delete, user_view,
    get_provinces, get_cities, get_barangays, upload_document, add_property_tax, update_property_tax, AllTaxRecordsView,
    ai_chat_api, ai_usage_api, TitleMovementListView, add_title_movement, generate_transmittal_number, UpdateTitleMovementStatusView,
    property_delete, tax_record_delete, movement_delete
)

urlpatterns = [
    # Title Movements
    path('movements/', TitleMovementListView.as_view(), name='movement_list'),
    path('api/generate-tm-number/', generate_transmittal_number, name='generate_transmittal_number'),
    path('api/movements/update-status/', UpdateTitleMovementStatusView.as_view(), name='update_title_movement_status'),

    # AI Chat API
    path('api/ai-chat/', ai_chat_api, name='ai_chat_api'),
    path('api/ai-usage/', ai_usage_api, name='ai_usage_api'),

    # Landing page: Login is now handled by root redirect to /accounts/login/
    # logout is still handled locally if needed, or can use django.contrib.auth.urls
    path('logout/', logout_view, name='app_logout'),
    
    # Dashboard on a separate route
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    
    # 2. Add Property View
    path('add-property/', PropertyCreateView.as_view(), name='add_property'),
    
    # 2.5 Update Property View
    path('property/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_update'),
    path('property/<int:pk>/delete/', property_delete, name='property_delete'),

    # 3. Property Detail View
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    
    # 3.5 Upload Document View
    path('property/<int:pk>/upload-document/', upload_document, name='upload_document'),

    # 3.6 Add Property Tax View
    path('property/<int:pk>/add-tax/', add_property_tax, name='add_property_tax'),
    path('tax/<int:pk>/update/', update_property_tax, name='update_property_tax'),
    path('tax/<int:pk>/delete/', tax_record_delete, name='tax_record_delete'),

    # 3.7 Add Title Movement View
    path('property/<int:pk>/add-movement/', add_title_movement, name='add_title_movement'),
    path('movement/<int:pk>/delete/', movement_delete, name='movement_delete'),
        
    # 4. Property List View: This is now moved to a new path to free up the root ('')
    path('properties/', PropertyListView.as_view(), name='property_list'), 
    path('all-tax-records/', AllTaxRecordsView.as_view(), name='all_tax_records'),
    
    # 5. Global Search API
    path('api/search/', global_search, name='global_search'),
    path('api/notifications/', notifications_api, name='notifications_api'),
    path('api/notifications/mark-read/', mark_notifications_read, name='mark_notifications_read'),
    path('api/notifications/clear-all/', clear_all_notifications, name='clear_all_notifications'),
    
    # Locations API (Proxied)
    path('api/locations/provinces/', get_provinces, name='get_provinces'),
    path('api/locations/cities/<str:province_code>/', get_cities, name='get_cities'),
    path('api/locations/barangays/<str:city_code>/', get_barangays, name='get_barangays'),
    
    # 6. User Management
    path('user-management/', user_list, name='user_list'),
    path('user-management/add/', user_create, name='user_create'),
    path('user-management/<int:user_id>/view/', user_view, name='user_view'),
    path('user-management/<int:user_id>/edit/', user_update, name='user_update'),
    path('user-management/<int:user_id>/delete/', user_delete, name='user_delete'),
]
