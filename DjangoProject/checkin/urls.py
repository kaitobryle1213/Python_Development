# checkin/urls.py

from django.urls import path
from . import views


urlpatterns = [
    # Main check-in form/success
    path('', views.checkin_view, name='checkin_form'),
    path('success/<int:pk>/', views.checkin_success_view, name='checkin_success'),

    # Company management
    path('companies/', views.company_list_view, name='company_list'),
    
    # --- NEW: Company Edit and Delete Paths ---
    path('companies/edit/<int:pk>/', views.company_edit_view, name='edit_company'),
    path('companies/delete/<int:pk>/', views.company_delete_view, name='delete_company'),
    # ------------------------------------------

    # Report & Export
    path('report/', views.checkin_report_view, name='checkin_report'),    # Report display
    path('report/export/csv/', views.export_checkin_csv, name='export_checkin_csv'),    # Export action

    # User Management (Admin Only)
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_create_view, name='user_add'),
    path('users/edit/<int:pk>/', views.user_edit_view, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete_view, name='user_delete'),
]