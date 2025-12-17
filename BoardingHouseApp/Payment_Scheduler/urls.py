from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/dashboard_data/', views.dashboard_api, name='dashboard_api'),
    path('users/', views.user_management_view, name='users'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('customers/', views.customer_view, name='customers'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('payment/', views.payment_view, name='payment'),
    path('api/search_customers/', views.search_customers, name='search_customers'),
    path('api/get_balance/<int:customer_id>/', views.get_customer_balance, name='get_customer_balance'),
    path('api/process_payment/', views.process_payment, name='process_payment'),
    
    # Room URLs
    path('rooms/', views.room_view, name='rooms'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('api/search_rooms/', views.search_rooms, name='search_rooms'),

    path('logout/', views.logout_view, name='logout'),
]
