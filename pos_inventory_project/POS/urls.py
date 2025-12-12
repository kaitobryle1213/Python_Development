from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # POS Transactions
    path('transactions/', views.pos_list, name='pos_list'),
    path('transactions/create/', views.pos_create, name='pos_create'),
    path('transactions/<int:transaction_id>/', views.pos_view, name='pos_view'),
    path('transactions/<int:transaction_id>/close/', views.pos_close, name='pos_close'),
    path('transactions/<int:transaction_id>/cancel/', views.pos_cancel, name='pos_cancel'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_view, name='customer_view'),
    path('customers/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views.customer_delete, name='customer_delete'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_view, name='user_view'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Items
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:item_id>/', views.item_view, name='item_view'),
    path('items/<int:item_id>/edit/', views.item_edit, name='item_edit'),
]

