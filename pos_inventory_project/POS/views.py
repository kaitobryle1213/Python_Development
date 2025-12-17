from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction as db_transaction
from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from datetime import datetime
import json
from decimal import Decimal

from .models import CustomUser, POSTransaction, POSLineItem, Customer, Item

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'POS/login.html')

@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    """Dashboard view - accessible only to logged-in users"""
    context = {
        'user': request.user,
    }
    return render(request, 'POS/dashboard.html', context)

@login_required(login_url='login')
def pos_list(request):
    """List all POS transactions"""
    transactions = POSTransaction.objects.all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(document_status=status)
    
    # Search by transaction no or customer name
    search = request.GET.get('search')
    if search:
        transactions = transactions.filter(
            models.Q(transaction_no__icontains=search) |
            models.Q(customer_name__icontains=search)
        )
    
    context = {
        'transactions': transactions,
        'statuses': ['OPEN', 'CLOSED', 'CANCELED']
    }
    return render(request, 'POS/pos_list.html', context)

@login_required(login_url='login')
def pos_create(request):
    """Create a new POS transaction"""
    if request.method == 'POST':
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                action = data.get('action')
                
                if action == 'get_customer':
                    customer_code = data.get('customer_code', '').strip()
                    
                    # If customer_code is empty, return all customers
                    if not customer_code:
                        customers = Customer.objects.filter(status='ACTIVE').values(
                            'id', 'customer_code', 'customer_name', 'customer_address', 'customer_tin'
                        )
                        return JsonResponse({
                            'success': True,
                            'customers': list(customers)
                        })
                    
                    # Otherwise search for specific customer
                    try:
                        customer = Customer.objects.get(customer_code=customer_code)
                        return JsonResponse({
                            'success': True,
                            'customer': {
                                'code': customer.customer_code,
                                'name': customer.customer_name,
                                'address': customer.customer_address,
                                'tin': customer.customer_tin,
                            }
                        })
                    except Customer.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Customer not found'})
                
                elif action == 'get_item':
                    item_code = data.get('item_code', '').strip()
                    
                    # If item_code is empty, return all items
                    if not item_code:
                        items = Item.objects.all().values(
                            'id', 'item_code', 'item_description', 'unit_of_measure', 
                            'unit_cost', 'unit_selling_price', 'quantity_on_hand'
                        )
                        return JsonResponse({
                            'success': True,
                            'items': list(items)
                        })
                    
                    # Otherwise search for specific item
                    try:
                        item = Item.objects.get(item_code=item_code)
                        return JsonResponse({
                            'success': True,
                            'item': {
                                'code': item.item_code,
                                'description': item.item_description,
                                'uom': item.unit_of_measure,
                                'unit_cost': str(item.unit_cost),
                                'unit_selling_price': str(item.unit_selling_price),
                                'quantity_on_hand': item.quantity_on_hand,
                            }
                        })
                    except Item.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Item not found'})
                
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'})
        
        # Handle form submission
        else:
            try:
                with db_transaction.atomic():
                    # Generate transaction number
                    from django.utils import timezone
                    today = timezone.now().date()
                    count = POSTransaction.objects.filter(transaction_date=today).count()
                    transaction_no = f"TRX-{today.strftime('%Y%m%d')}-{count + 1:04d}"
                    
                    # Get customer data
                    customer_code = request.POST.get('customer_code')
                    customer = None
                    if customer_code:
                        customer = get_object_or_404(Customer, customer_code=customer_code)
                    
                    # Create transaction
                    pos_transaction = POSTransaction.objects.create(
                        transaction_no=transaction_no,
                        transaction_date=datetime.now().date(),
                        document_status='OPEN',
                        customer_code=customer,
                        customer_name=request.POST.get('customer_name', ''),
                        customer_address=request.POST.get('customer_address', ''),
                        customer_tin=request.POST.get('customer_tin', ''),
                        mode_of_payment=request.POST.get('mode_of_payment', 'CASH'),
                        created_by=request.user
                    )
                    
                    # Add line items from hidden inputs
                    line_items_data = request.POST.get('line_items', '[]')
                    try:
                        line_items = json.loads(line_items_data)
                        for item_data in line_items:
                            item = get_object_or_404(Item, item_code=item_data['item_code'])
                            subtotal = int(item_data['quantity']) * float(item_data['unit_selling_price'])
                            
                            POSLineItem.objects.create(
                                transaction=pos_transaction,
                                item_code=item,
                                item_description=item_data.get('item_description', item.item_description),
                                unit_of_measure=item_data.get('unit_of_measure', item.unit_of_measure),
                                quantity=item_data['quantity'],
                                unit_cost=item_data.get('unit_cost', item.unit_cost),
                                unit_selling_price=item_data['unit_selling_price'],
                                subtotal=subtotal
                            )
                    except (json.JSONDecodeError, ValueError):
                        pass
                    
                    pos_transaction.calculate_totals()
                    mode = request.POST.get('mode_of_payment', 'CASH')
                    pos_transaction.mode_of_payment = mode
                    if mode == 'CASH':
                        amount_received_str = request.POST.get('cash_amount_received', '').strip()
                        if not amount_received_str:
                            raise ValueError('Cash amount received is required for Cash payment.')
                        amount_received = Decimal(amount_received_str)
                        pos_transaction.cash_amount_received = amount_received
                        pos_transaction.cash_amount_change = amount_received - Decimal(pos_transaction.grand_total)
                    elif mode == 'CHECK':
                        check_number = request.POST.get('check_number', '').strip()
                        check_date_str = request.POST.get('check_date', '').strip()
                        check_amount_str = request.POST.get('check_amount', '').strip()
                        if not (check_number and check_date_str and check_amount_str):
                            raise ValueError('Check number, check date, and check amount are required for Check payment.')
                        pos_transaction.check_number = check_number
                        pos_transaction.check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date()
                        pos_transaction.check_amount = Decimal(check_amount_str)
                    elif mode == 'ONLINE':
                        bank_number = request.POST.get('bank_number', '').strip()
                        bank_code = request.POST.get('bank_code', '').strip()
                        online_date_str = request.POST.get('online_transaction_date', '').strip()
                        if not (bank_number and bank_code and online_date_str):
                            raise ValueError('Bank number, bank code, and transaction date are required for Online Transfer.')
                        pos_transaction.bank_number = bank_number
                        pos_transaction.bank_code = bank_code
                        pos_transaction.online_transaction_date = datetime.strptime(online_date_str, '%Y-%m-%d').date()
                    pos_transaction.save()
                    messages.success(request, f'Transaction {transaction_no} created successfully!')
                    return redirect('pos_view', transaction_id=pos_transaction.id)
            
            except Exception as e:
                messages.error(request, f'Error creating transaction: {str(e)}')
    
    # GET request - show form
    customers = Customer.objects.all()
    items = Item.objects.all()
    
    context = {
        'customers': customers,
        'items': items,
    }
    return render(request, 'POS/pos_form.html', context)

@login_required(login_url='login')
def pos_view(request, transaction_id):
    """View POS transaction details"""
    pos_transaction = get_object_or_404(POSTransaction, id=transaction_id)
    line_items = POSLineItem.objects.filter(transaction=pos_transaction)
    
    # Check if user can edit (only if OPEN)
    can_edit = request.user == pos_transaction.created_by or request.user.is_manager
    
    context = {
        'transaction': pos_transaction,
        'line_items': line_items,
        'can_edit': can_edit,
    }
    return render(request, 'POS/pos_view.html', context)

@login_required(login_url='login')
def pos_close(request, transaction_id):
    """Close a POS transaction"""
    pos_transaction = get_object_or_404(POSTransaction, id=transaction_id)
    
    if request.user != pos_transaction.created_by and not request.user.is_manager:
        messages.error(request, 'You do not have permission to close this transaction.')
        return redirect('pos_view', transaction_id=transaction_id)
    
    if request.method == 'POST':
        pos_transaction.document_status = 'CLOSED'
        pos_transaction.save()
        messages.success(request, f'Transaction {pos_transaction.transaction_no} closed successfully!')
        return redirect('pos_view', transaction_id=transaction_id)
    
    context = {'transaction': pos_transaction}
    return render(request, 'POS/pos_close_confirm.html', context)

@login_required(login_url='login')
def pos_cancel(request, transaction_id):
    """Cancel a POS transaction"""
    pos_transaction = get_object_or_404(POSTransaction, id=transaction_id)
    
    if request.user != pos_transaction.created_by and not request.user.is_manager:
        messages.error(request, 'You do not have permission to cancel this transaction.')
        return redirect('pos_view', transaction_id=transaction_id)
    
    
    if request.method == 'POST':
        pos_transaction.document_status = 'CANCELED'
        pos_transaction.save()
        messages.success(request, f'Transaction {pos_transaction.transaction_no} canceled!')
        return redirect('pos_list')
    
    context = {'transaction': pos_transaction}
    return render(request, 'POS/pos_cancel_confirm.html', context)


# ===== CUSTOMER MANAGEMENT VIEWS =====

@login_required(login_url='login')
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        customers = customers.filter(status=status)
    
    # Filter by type if provided
    customer_type = request.GET.get('type')
    if customer_type:
        customers = customers.filter(customer_type=customer_type)
    
    # Search by name or code
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            models.Q(customer_code__icontains=search) | 
            models.Q(customer_name__icontains=search)
        )
    
    context = {
        'customers': customers,
        'statuses': ['ACTIVE', 'INACTIVE'],
        'types': ['WALKIN', 'REGULAR', 'SUPPLIER'],
    }
    return render(request, 'POS/customer_list.html', context)


@login_required(login_url='login')
def customer_create(request):
    """Create a new customer"""
    if request.method == 'POST':
        try:
            customer_code = request.POST.get('customer_code', '').strip()
            customer_name = request.POST.get('customer_name', '').strip()
            customer_type = request.POST.get('customer_type', 'WALKIN')
            customer_address = request.POST.get('customer_address', '').strip()
            customer_tin = request.POST.get('customer_tin', '').strip()
            status = request.POST.get('status', 'ACTIVE')
            date_entry = request.POST.get('date_entry')
            
            # Validation
            if not customer_code or not customer_name:
                messages.error(request, 'Customer code and name are required.')
                return redirect('customer_create')
            
            # Check if code already exists
            if Customer.objects.filter(customer_code=customer_code).exists():
                messages.error(request, f'Customer code {customer_code} already exists.')
                return redirect('customer_create')
            
            # Create customer
            customer = Customer.objects.create(
                customer_code=customer_code,
                customer_name=customer_name,
                customer_type=customer_type,
                customer_address=customer_address,
                customer_tin=customer_tin,
                status=status,
                date_entry=date_entry or timezone.now().date()
            )
            
            messages.success(request, f'Customer {customer_code} created successfully!')
            return redirect('customer_view', customer_id=customer.id)
        
        except Exception as e:
            messages.error(request, f'Error creating customer: {str(e)}')
    
    context = {
        'types': Customer.CUSTOMER_TYPE_CHOICES,
        'statuses': Customer.STATUS_CHOICES,
        'today': timezone.now().date(),
    }
    return render(request, 'POS/customer_form.html', context)


@login_required(login_url='login')
def customer_view(request, customer_id):
    """View customer details"""
    customer = get_object_or_404(Customer, id=customer_id)
    context = {'customer': customer}
    return render(request, 'POS/customer_view.html', context)


@login_required(login_url='login')
def customer_edit(request, customer_id):
    """Edit customer details"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        try:
            customer.customer_name = request.POST.get('customer_name', '').strip()
            customer.customer_type = request.POST.get('customer_type', 'WALKIN')
            customer.customer_address = request.POST.get('customer_address', '').strip()
            customer.customer_tin = request.POST.get('customer_tin', '').strip()
            customer.status = request.POST.get('status', 'ACTIVE')
            customer.date_entry = request.POST.get('date_entry', customer.date_entry)
            
            if not customer.customer_name:
                messages.error(request, 'Customer name is required.')
                return redirect('customer_edit', customer_id=customer.id)
            
            customer.save()
            messages.success(request, f'Customer {customer.customer_code} updated successfully!')
            return redirect('customer_view', customer_id=customer.id)
        
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
    
    context = {
        'customer': customer,
        'types': Customer.CUSTOMER_TYPE_CHOICES,
        'statuses': Customer.STATUS_CHOICES,
        'is_edit': True,
    }
    return render(request, 'POS/customer_form.html', context)


@login_required(login_url='login')
def customer_delete(request, customer_id):
    """Delete customer - will cascade delete any linked transactions"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer_code = customer.customer_code
        # This will also delete any linked transactions due to CASCADE
        customer.delete()
        messages.success(request, f'Customer {customer_code} and any linked transactions have been deleted successfully!')
        return redirect('customer_list')
    
    context = {'customer': customer}
    return render(request, 'POS/customer_delete_confirm.html', context)


# ===== USER MANAGEMENT VIEWS =====

@login_required(login_url='login')
def user_list(request):
    """List all users (managers only)"""
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, 'You do not have permission to access user management.')
        return redirect('dashboard')
    
    users = CustomUser.objects.all()
    
    # Filter by role if provided
    role = request.GET.get('role')
    if role == 'cashier':
        users = users.filter(is_cashier=True)
    elif role == 'manager':
        users = users.filter(is_manager=True)
    
    # Search by username or name
    search = request.GET.get('search')
    if search:
        users = users.filter(
            models.Q(username__icontains=search) | 
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search)
        )
    
    context = {
        'users': users,
    }
    return render(request, 'POS/user_list.html', context)


@login_required(login_url='login')
def user_create(request):
    """Create a new user (managers only)"""
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, 'You do not have permission to create users.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            complete_name = request.POST.get('complete_name', '').strip()
            password = request.POST.get('password', '').strip()
            password_confirm = request.POST.get('password_confirm', '').strip()
            role = request.POST.get('role', 'User')
            status = request.POST.get('status', 'Active')
            
            # Validation
            if not username or not password:
                messages.error(request, 'Username and password are required.')
                return redirect('user_create')
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return redirect('user_create')
            
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already exists.')
                return redirect('user_create')
            
            # Split complete name into first and last name
            name_parts = complete_name.split(' ', 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_manager=(role == 'Admin'),
                is_active=(status == 'Active'),
            )
            
            messages.success(request, f'User {username} created successfully!')
            return redirect('user_view', user_id=user.id)
        
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    context = {}
    return render(request, 'POS/user_form.html', context)


@login_required(login_url='login')
def user_view(request, user_id):
    """View user details (managers only)"""
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, 'You do not have permission to view user details.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    context = {'user': user}
    return render(request, 'POS/user_view.html', context)


@login_required(login_url='login')
def user_edit(request, user_id):
    """Edit user details (managers only)"""
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        try:
            complete_name = request.POST.get('complete_name', '').strip()
            role = request.POST.get('role', 'User')
            status = request.POST.get('status', 'Active')
            
            # Split complete name into first and last name
            name_parts = complete_name.split(' ', 1)
            user.first_name = name_parts[0] if len(name_parts) > 0 else ''
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            user.is_manager = (role == 'Admin')
            user.is_active = (status == 'Active')
            
            new_password = request.POST.get('password', '').strip()
            password_confirm = request.POST.get('password_confirm', '').strip()
            
            if new_password:
                if new_password != password_confirm:
                    messages.error(request, 'Passwords do not match.')
                    return redirect('user_edit', user_id=user.id)
                user.set_password(new_password)
            
            user.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('user_view', user_id=user.id)
        
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    context = {'user': user, 'is_edit': True}
    return render(request, 'POS/user_form.html', context)


@login_required(login_url='login')
def user_delete(request, user_id):
    """Delete a user (managers only)"""
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('user_list')
    
    context = {'user': user}
    return render(request, 'POS/user_delete_confirm.html', context)


# ===== ITEM MANAGEMENT VIEWS =====

@login_required(login_url='login')
def item_list(request):
    """List all items"""
    items = Item.objects.all()
    
    # Search by code or description
    search = request.GET.get('search')
    if search:
        items = items.filter(
            models.Q(item_code__icontains=search) | 
            models.Q(item_description__icontains=search)
        )
    
    # Filter by unit of measure
    uom = request.GET.get('uom')
    if uom:
        items = items.filter(unit_of_measure=uom)
    
    # Filter by stock level
    stock = request.GET.get('stock')
    if stock == 'low':
        items = items.filter(quantity_on_hand__lte=5)
    elif stock == 'in':
        items = items.filter(quantity_on_hand__gt=5)
    
    context = {
        'items': items,
        'units': Item.UNIT_CHOICES,
    }
    return render(request, 'POS/item_list.html', context)


@login_required(login_url='login')
def item_create(request):
    """Create a new item"""
    if request.method == 'POST':
        try:
            item_code = request.POST.get('item_code', '').strip()
            item_description = request.POST.get('item_description', '').strip()
            unit_of_measure = request.POST.get('unit_of_measure', '')
            unit_cost = request.POST.get('unit_cost', '0')
            unit_selling_price = request.POST.get('unit_selling_price', '0')
            quantity_on_hand = request.POST.get('quantity_on_hand', '0')
            
            # Validation
            if not item_code or not item_description:
                messages.error(request, 'Item code and description are required.')
                return redirect('item_create')
            
            if Item.objects.filter(item_code=item_code).exists():
                messages.error(request, f'Item code {item_code} already exists.')
                return redirect('item_create')
            
            # Create item
            item = Item.objects.create(
                item_code=item_code,
                item_description=item_description,
                unit_of_measure=unit_of_measure,
                unit_cost=unit_cost,
                unit_selling_price=unit_selling_price,
                quantity_on_hand=quantity_on_hand,
            )
            
            messages.success(request, f'Item {item_code} created successfully!')
            return redirect('item_view', item_id=item.id)
        
        except Exception as e:
            messages.error(request, f'Error creating item: {str(e)}')
    
    context = {
        'units': Item.UNIT_CHOICES,
    }
    return render(request, 'POS/item_form.html', context)


@login_required(login_url='login')
def item_view(request, item_id):
    """View item details"""
    item = get_object_or_404(Item, id=item_id)
    context = {'item': item}
    return render(request, 'POS/item_view.html', context)


@login_required(login_url='login')
def item_edit(request, item_id):
    """Edit item details"""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        try:
            item.item_description = request.POST.get('item_description', '').strip()
            item.unit_of_measure = request.POST.get('unit_of_measure', '')
            item.unit_cost = request.POST.get('unit_cost', item.unit_cost)
            item.unit_selling_price = request.POST.get('unit_selling_price', item.unit_selling_price)
            item.quantity_on_hand = request.POST.get('quantity_on_hand', item.quantity_on_hand)
            
            if not item.item_description:
                messages.error(request, 'Item description is required.')
                return redirect('item_edit', item_id=item.id)
            
            item.save()
            messages.success(request, f'Item {item.item_code} updated successfully!')
            return redirect('item_view', item_id=item.id)
        
        except Exception as e:
            messages.error(request, f'Error updating item: {str(e)}')
    
    context = {
        'item': item,
        'units': Item.UNIT_CHOICES,
        'is_edit': True,
    }
    return render(request, 'POS/item_form.html', context)


@login_required(login_url='login')
def item_delete(request, item_id):
    """Delete an item (with protection if referenced by transactions)"""
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, f'Item {item.item_code} deleted successfully!')
            return redirect('item_list')
        except ProtectedError:
            messages.error(request, 'Cannot delete this item because it is referenced by transactions.')
            return redirect('item_view', item_id=item.id)
        except Exception as e:
            messages.error(request, f'Error deleting item: {str(e)}')
            return redirect('item_view', item_id=item.id)
    return render(request, 'POS/item_delete_confirm.html', {'item': item})
