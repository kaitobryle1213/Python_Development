from django.contrib import admin
from .models import CustomUser, Customer, Item, POSTransaction, POSLineItem

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'is_cashier', 'is_manager')
    list_filter = ('is_cashier', 'is_manager')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'customer_name', 'customer_type', 'status', 'date_entry')
    list_filter = ('customer_type', 'status', 'date_entry')
    search_fields = ('customer_code', 'customer_name', 'customer_tin')
    ordering = ('-date_entry',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'item_description', 'unit_of_measure', 'unit_cost', 'unit_selling_price', 'quantity_on_hand')
    list_filter = ('unit_of_measure',)
    search_fields = ('item_code', 'item_description')
    ordering = ('item_description',)

@admin.register(POSTransaction)
class POSTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_no', 'transaction_date', 'customer_name', 'document_status', 'grand_total', 'created_by')
    list_filter = ('document_status', 'transaction_date')
    search_fields = ('transaction_no', 'customer_name', 'customer_code__customer_code')
    readonly_fields = ('transaction_no', 'created_at', 'updated_at', 'subtotal', 'grand_total')
    ordering = ('-transaction_date', '-transaction_no')

@admin.register(POSLineItem)
class POSLineItemAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'item_code', 'quantity', 'unit_selling_price', 'subtotal')
    list_filter = ('transaction__transaction_date',)
    search_fields = ('transaction__transaction_no', 'item_code__item_code')
    readonly_fields = ('subtotal',)
