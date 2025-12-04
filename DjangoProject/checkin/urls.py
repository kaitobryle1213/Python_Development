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
]