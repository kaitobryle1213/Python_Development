from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Payment, BoardingHouseUser, Room
from .forms import CustomerForm, BoardingHouseUserForm, BoardingHouseUserEditForm, RoomForm
from datetime import date, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Count, F, Sum
from django.db.models import Max
from django.db.models import Prefetch
from dateutil.relativedelta import relativedelta
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Room

# --- AUTHENTICATION ---

def is_admin(user):
    return user.role == 'Admin'

admin_required = user_passes_test(is_admin, login_url='dashboard')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'Payment_Scheduler/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- DASHBOARD & SCHEDULE ---

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    # Calculate stats
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(status='Active').count()
    occupied_rooms = Customer.objects.filter(status='Active').exclude(room=None).count() # Or use Room model logic
    
    # Calculate revenue
    monthly_revenue = Payment.objects.filter(
        date_paid__year=today.year,
        date_paid__month=today.month,
        is_paid=True
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    customers = Customer.objects.all().select_related('room').prefetch_related('payments')
    
    # Prepare data for template
    customer_data = []
    for customer in customers:
        last_payment = customer.payments.filter(is_paid=True).order_by('-date_paid').first()
        is_paid_today = last_payment and last_payment.date_paid == today

        if is_paid_today:
            color = 'green'
            status_text = "Paid"
        elif customer.due_date:
            days_until_due = (customer.due_date - today).days
            if days_until_due < 0:
                color = 'black'
                status_text = "Overdue"
            elif days_until_due == 0:
                color = 'red'
                status_text = "Due Today"
            elif days_until_due <= 5: 
                color = 'yellow'
                status_text = "Due Soon"
            else:
                color = 'white'
                status_text = "Upcoming"
        else:
            color = 'white'
            status_text = "No Schedule"

        customer_data.append({
            'customer': customer,
            'color': color,
            'status_text': status_text,
            'last_payment_date': last_payment.date_paid if last_payment else None
        })

    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'occupied_rooms': occupied_rooms,
        'monthly_revenue': monthly_revenue,
        'customers': customer_data,
        'today': today,
    }
    return render(request, 'Payment_Scheduler/dashboard.html', context)


# --- ROOM MANAGEMENT ---

@login_required
@admin_required
def room_view(request):
    rooms = (
        Room.objects.annotate(
            active_customers_count=Count(
                'customers',
                filter=Q(customers__status='Active')
            )
        )
        .order_by('room_number')
    )
    
    # Auto-sync room.status based on occupancy (excluding 'Under Maintenance')
    for r in rooms:
        if r.status != 'Under Maintenance':
            new_status = 'Available' if r.active_customers_count == 0 else 'Occupied'
            if r.status != new_status:
                r.status = new_status
                r.save(update_fields=['status'])
    
    return render(request, 'Payment_Scheduler/room.html', {'rooms': rooms})

@login_required
@admin_required
def room_list(request):
    # This specifically counts customers per room whose status is 'Active'
    rooms = Room.objects.annotate(
        active_customers_count=Count(
            'customers', 
            filter=Q(customers__status='Active')
        )
    ).order_by('room_number')
    
    return render(request, 'Payment_Scheduler/room.html', {'rooms': rooms})

@login_required
@admin_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    else:
        form = RoomForm()
    return render(request, 'Payment_Scheduler/room_form.html', {'form': form, 'title': 'Create Room'})

@login_required
@admin_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'Payment_Scheduler/room_form.html', {'form': form, 'title': 'Edit Room'})

# ... (existing imports)

@login_required
@admin_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Filter only Active customers
    occupants = room.customers.filter(status='Active')
    occupant_count = occupants.count()

    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            if occupant_count == 0:
                room.delete()
                return redirect('rooms')
        
        elif 'transfer_delete' in request.POST:
            new_room_id = request.POST.get('new_room')
            if new_room_id:
                new_room = get_object_or_404(Room, pk=new_room_id)
                
                # Bulk update room for all occupants
                occupants.update(room=new_room)
                
                # Update new room status
                # Check if new room is now full or just occupied
                new_room_occupants = Customer.objects.filter(room=new_room, status='Active').count()
                if new_room_occupants >= new_room.capacity:
                    new_room.status = 'Full'
                else:
                    new_room.status = 'Occupied'
                new_room.save(update_fields=['status'])
                
                room.delete()
                return redirect('rooms')

    # GET request: Prepare context for confirmation page
    # Find available rooms with capacity > current_occupants
    # We use Python filtering to avoid MySQL HAVING clause issues with F() expressions
    all_rooms = Room.objects.exclude(pk=room.pk).exclude(status='Under Maintenance').annotate(
        active_count=Count('customers', filter=Q(customers__status='Active'))
    )
    
    available_rooms = [r for r in all_rooms if r.active_count < r.capacity]
    
    context = {
        'room': room,
        'occupant_count': occupant_count,
        'available_rooms': available_rooms,
        'has_vacant_rooms': len(available_rooms) > 0
    }
    return render(request, 'Payment_Scheduler/room_delete.html', context)

@login_required
@admin_required
def room_occupants(request, pk):
    room = get_object_or_404(Room, pk=pk)
    occupants = room.customers.filter(status='Active')
    
    # Get available rooms for transfer (excluding current one)
    # Python filtering to avoid MySQL errors
    all_rooms = Room.objects.exclude(pk=room.pk).exclude(status='Under Maintenance').annotate(
        active_count=Count('customers', filter=Q(customers__status='Active'))
    )
    
    available_rooms = [r for r in all_rooms if r.active_count < r.capacity]
    
    return render(request, 'Payment_Scheduler/room_occupants.html', {
        'room': room,
        'occupants': occupants,
        'available_rooms': available_rooms
    })

@login_required
@admin_required
def transfer_customer(request, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=customer_id)
        old_room = customer.room
        new_room_id = request.POST.get('new_room')
        
        if new_room_id:
            new_room = get_object_or_404(Room, pk=new_room_id)
            
            # Update customer room
            customer.room = new_room
            customer.save()
            
            # Update old room status
            if old_room:
                old_room_active = Customer.objects.filter(room=old_room, status='Active').count()
                if old_room_active == 0:
                    old_room.status = 'Available'
                else:
                    # Check if it was full and now is just occupied
                    if old_room.status == 'Full':
                        old_room.status = 'Occupied'
                old_room.save(update_fields=['status'])
                
            # Update new room status
            new_room_active = Customer.objects.filter(room=new_room, status='Active').count()
            if new_room_active >= new_room.capacity:
                new_room.status = 'Full'
            else:
                new_room.status = 'Occupied'
            new_room.save(update_fields=['status'])
            
            return redirect('room_occupants', pk=old_room.pk if old_room else new_room.pk)
            
    return redirect('rooms')

@login_required
@admin_required
def search_rooms(request):
    query = request.GET.get('q', '')
    
    # Filter for rooms that are NOT Under Maintenance
    rooms_qs = Room.objects.exclude(status='Under Maintenance').annotate(
        current_occupants=Count('customers', filter=Q(customers__status='Active'))
    )

    if query:
        rooms_qs = rooms_qs.filter(room_number__icontains=query)
        
    # Python filtering to avoid MySQL errors
    rooms = [r for r in rooms_qs if r.current_occupants < r.capacity]

    results = []
    for r in rooms:
        # We also want to make sure the room status is 'Available' 
        # if it was previously 'Occupied' but now has 0 people.
        results.append({
            'id': r.id, 
            'room_number': r.room_number, 
            'room_type': r.room_type, 
            'price': str(r.price),
            'status': r.status,
            'available_slots': r.capacity - r.current_occupants
        })
    
    return JsonResponse(results, safe=False)


# --- USER MANAGEMENT ---

@login_required
@admin_required
def user_management_view(request):
    users = BoardingHouseUser.objects.all()
    return render(request, 'Payment_Scheduler/user.html', {'users': users})

@login_required
@admin_required
def user_create(request):
    if request.method == 'POST':
        form = BoardingHouseUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = BoardingHouseUserForm()
    return render(request, 'Payment_Scheduler/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
@admin_required
def user_edit(request, pk):
    user_obj = get_object_or_404(BoardingHouseUser, pk=pk)
    if request.method == 'POST':
        form = BoardingHouseUserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = BoardingHouseUserEditForm(instance=user_obj)
    return render(request, 'Payment_Scheduler/user_form.html', {'form': form, 'title': 'Edit User'})


# --- CUSTOMER MANAGEMENT ---

@login_required
@admin_required
def customer_view(request):
    customers = Customer.objects.annotate(last_paid=Max('payments__date_paid')).order_by('-date_entry', '-last_paid')[:12]
    return render(request, 'Payment_Scheduler/customer.html', {'customers': customers})

@login_required
@admin_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            instance = form.save()
            
            # Update room status after assignment
            if instance.room:
                occupants = Customer.objects.filter(room=instance.room, status='Active').count()
                new_status = 'Available' if occupants == 0 else 'Occupied'
                if instance.room.status != 'Under Maintenance' and instance.room.status != new_status:
                    instance.room.status = new_status
                    instance.room.save(update_fields=['status'])
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'Payment_Scheduler/customer_form.html', {'form': form, 'title': 'Create Customer'})

@login_required
@admin_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            instance = form.save(commit=False)
            old_room = customer.room
            
            if instance.status == 'Inactive':
                # Store the room reference before we clear it
                vacated_room = instance.room
                
                if not instance.date_left:
                    instance.date_left = timezone.now().date()
                
                # 1. Remove the customer from the room
                instance.room = None 
                
                # 2. Check if the room is now empty and update its status
                if vacated_room:
                    # Count remaining active customers in that specific room
                    remaining_occupants = Customer.objects.filter(room=vacated_room, status='Active').exclude(pk=instance.pk).count()
                    
                    if remaining_occupants == 0:
                        vacated_room.status = 'Available'
                        vacated_room.save()
            
            instance.save()
            
            # If still active, sync statuses for new and old rooms
            if instance.status == 'Active':
                # Update newly assigned room status
                if instance.room:
                    occupants = Customer.objects.filter(room=instance.room, status='Active').count()
                    new_status = 'Available' if occupants == 0 else 'Occupied'
                    if instance.room.status != 'Under Maintenance' and instance.room.status != new_status:
                        instance.room.status = new_status
                        instance.room.save(update_fields=['status'])
                
                # If room changed, update old room status as well
                if old_room and old_room != instance.room:
                    old_occupants = Customer.objects.filter(room=old_room, status='Active').count()
                    old_status = 'Available' if old_occupants == 0 else 'Occupied'
                    if old_room.status != 'Under Maintenance' and old_room.status != old_status:
                        old_room.status = old_status
                        old_room.save(update_fields=['status'])
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'Payment_Scheduler/customer_form.html', {'form': form, 'title': 'Edit Customer'})

@login_required
@admin_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'Payment_Scheduler/customer_detail.html', {'customer': customer})

@login_required
@admin_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        room = customer.room
        customer.delete()
        
        # Update room status if it becomes empty
        if room:
            # Check remaining active customers
            active_occupants = Customer.objects.filter(room=room, status='Active').count()
            if active_occupants == 0:
                room.status = 'Available'
                room.save(update_fields=['status'])
                
        return redirect('customers')
    return redirect('customers')



# --- PAYMENT PROCESSING ---

@login_required
@admin_required
def payment_view(request):
    return render(request, 'Payment_Scheduler/payment.html')

@login_required
@admin_required
def search_customers(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | 
            Q(room__room_number__icontains=query)
        )[:10]
        results = []
        for c in customers:
            results.append({
                'id': c.pk,
                'display_id': c.customer_id,
                'name': c.name,
                'room_no': c.room.room_number if c.room else "N/A",
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
@admin_required
def get_customer_balance(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    payment = Payment.objects.filter(customer=customer, due_date=customer.due_date, is_paid=False).first()
    
    if customer.due_date:
        due_date_str = customer.due_date.strftime('%Y-%m-%d')
    else:
        due_date_str = timezone.now().date().strftime('%Y-%m-%d')

    cycle_paid = Payment.objects.filter(
        customer=customer,
        due_date=customer.due_date,
        is_paid=True
    ).aggregate(Sum('amount_received'))['amount_received__sum'] or 0
    total_due = customer.room.price if customer.room else 0
    remaining_balance = max(total_due - cycle_paid, 0)

    return JsonResponse({
        'customer_id': customer.customer_id,
        'customer_db_id': customer.pk,
        'name': customer.name,
        'room_no': customer.room.room_number if customer.room else (customer.room_number if customer.room_number else "N/A"),
        'payment_id': payment.id if payment else "", 
        'due_date': due_date_str,
        'balance': remaining_balance,
    })

@login_required
def dashboard_api(request):
    limit = int(request.GET.get('limit', 12))
    offset = int(request.GET.get('offset', 0))
    sort = request.GET.get('sort', 'latest_payment')
    base_qs = Customer.objects.all().annotate(last_paid=Max('payments__date_paid')).select_related('room').prefetch_related(
        Prefetch('payments', queryset=Payment.objects.filter(is_paid=True).only('amount_received', 'due_date', 'date_paid', 'remarks'))
    )
    if sort == 'latest_entry':
        base_qs = base_qs.order_by('-date_entry', '-last_paid')
    else:
        base_qs = base_qs.order_by('-last_paid', '-date_entry')
    total = base_qs.count()
    customers = base_qs[offset:offset + limit]
    today = timezone.now().date()
    data = []
    
    for customer in customers:
        effective_due = None
        if customer.due_date:
            if customer.due_date < today:
                effective_due = customer.due_date + relativedelta(months=1)
            else:
                effective_due = customer.due_date

        paid_payments = list(customer.payments.all())
        last_payment_date = None
        if paid_payments:
            last_payment_date = max((p.date_paid for p in paid_payments if p.date_paid), default=None)
        is_paid_today = last_payment_date == today

        cycle_paid = 0
        if effective_due:
            cycle_paid = sum((p.amount_received or 0) for p in paid_payments if p.due_date == effective_due)
        price = customer.room.price if customer.room else 0
        balance_amount = max(price - cycle_paid, 0)

        if is_paid_today and cycle_paid >= price and price > 0:
            color, status = 'green', "Paid"
        elif effective_due:
            days = (effective_due - today).days
            if days < 0: color, status = 'black', "Overdue"
            elif days == 0: color, status = 'red', "Due Today"
            elif days <= 3: color, status = 'yellow', "Due Soon"
            else: color, status = 'white', "Upcoming"
        else:
            color, status = 'white', "No Schedule"

        if price > 0 and cycle_paid > 0 and cycle_paid < price:
            status = f"Partially Paid • Balance: ₱{balance_amount}"
        elif price > 0 and cycle_paid >= price:
            status = "Paid"

        data.append({
            'name': customer.name,
            'room_no': customer.room.room_number if customer.room else (customer.room_no or "-"),
            'prev_payment': last_payment_date.strftime('%b %d, %Y') if last_payment_date else "-",
            'due_date': effective_due.strftime('%b %d, %Y') if effective_due else "N/A",
            'room_rate': f"₱{price}" if customer.room else "-",
            'amount': f"₱{cycle_paid}" if cycle_paid else "-",
            'status': status,
            'color': color
        })
    has_more = (offset + limit) < total
    next_offset = offset + limit if has_more else None
    return JsonResponse({'payment_data': data, 'has_more': has_more, 'next_offset': next_offset, 'total': total})

@login_required
@admin_required
def customers_api(request):
    limit = int(request.GET.get('limit', 12))
    offset = int(request.GET.get('offset', 0))
    sort = request.GET.get('sort', 'latest_entry')
    qs = Customer.objects.all().annotate(last_paid=Max('payments__date_paid')).select_related('room')
    if sort == 'latest_payment':
        qs = qs.order_by('-last_paid', '-date_entry')
    else:
        qs = qs.order_by('-date_entry', '-last_paid')
    total = qs.count()
    items = []
    for c in qs[offset:offset + limit]:
        items.append({
            'id': c.pk,
            'customer_id': c.customer_id,
            'name': c.name,
            'address': c.address or "",
            'contact_number': c.contact_number or "",
            'parents_name': c.parents_name or "",
            'parents_contact_number': c.parents_contact_number or "",
            'status': c.status or "",
            'room': c.room.room_number if c.room else (c.room_no or "-"),
            'date_entry': c.date_entry.strftime('%b %d, %Y') if c.date_entry else "-",
            'due_date': c.due_date.strftime('%b %d, %Y') if c.due_date else "-",
        })
    has_more = (offset + limit) < total
    next_offset = offset + limit if has_more else None
    return JsonResponse({'customers': items, 'has_more': has_more, 'next_offset': next_offset, 'total': total})

@login_required
@admin_required
def process_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        customer_id = request.POST.get('customer_id') 
        amount_received = request.POST.get('amount_received')
        change_amount = request.POST.get('change_amount')
        remarks = request.POST.get('remarks')
        
        try:
            customer = Customer.objects.get(pk=customer_id)
            
            if payment_id and payment_id.strip() != "":
                payment = Payment.objects.get(pk=payment_id)
            else:
                payment = Payment(
                    customer=customer,
                    amount=customer.room.price if customer.room else 0,
                    due_date=customer.due_date or timezone.now().date()
                )

            # Record the previous payment date (what was seen on dashboard)
            # Only if we are marking it paid now (it was not paid before)
            # Update: User requested to save the current date_paid into previous_date as well
            payment.date_paid = timezone.now().date()
            payment.previous_date = payment.date_paid
            
            payment.amount_received = amount_received
            payment.change_amount = change_amount
            payment.remarks = remarks
            payment.is_paid = True
            payment.save()
            
            if customer.due_date and timezone.now().date() > customer.due_date:
                customer.due_date = customer.due_date + relativedelta(months=1)
                customer.save(update_fields=['due_date'])
            
            return JsonResponse({'success': True})
            
        except (Payment.DoesNotExist, Customer.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@admin_required
def report_view(request):
    today = timezone.now().date()
    customers = Customer.objects.select_related('room').prefetch_related('payments').all()

    # Filters
    room_id = request.GET.get('room')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    customer_name = request.GET.get('customer_name')

    if room_id:
        customers = customers.filter(room__id=room_id)
    if customer_name:
        customers = customers.filter(name__icontains=customer_name)

    rows = []
    total_collected = 0

    for c in customers:
        # Advance due date only after it passes (keep cycles aligned)
        if c.due_date and c.due_date < today:
            c.due_date = c.due_date + relativedelta(months=1)
            c.save(update_fields=['due_date'])

        price = c.room.price if c.room else 0
        cycle_qs = Payment.objects.filter(customer=c, due_date=c.due_date, is_paid=True)
        cycle_sum = cycle_qs.aggregate(Sum('amount_received'))['amount_received__sum'] or 0
        last_paid = cycle_qs.order_by('-date_paid').first()

        # Optional date filters apply to the last payment date for inclusion
        if date_from and last_paid and str(last_paid.date_paid) < date_from:
            continue
        if date_to and last_paid and str(last_paid.date_paid) > date_to:
            continue

        balance = max(price - cycle_sum, 0)
        if price > 0 and cycle_sum >= price:
            status = "Paid"
        elif cycle_sum > 0:
            status = f"Partially Paid • Balance: ₱{balance}"
        else:
            status = "Unpaid"

        total_collected += cycle_sum

        rows.append({
            'name': c.name,
            'contact_number': c.contact_number,
            'parents_name': c.parents_name,
            'parents_contact_number': c.parents_contact_number,
            'room_no': c.room.room_number if c.room else (c.room_no or "-"),
            'date_entry': c.date_entry,
            'due_date': c.due_date,
            'paid_amount': cycle_sum,
            'date_amount_paid': last_paid.date_paid if last_paid else None,
            'remarks': last_paid.remarks if last_paid and last_paid.remarks else "",
            'status': status,
        })

    total_amount = "{:,.2f}".format(total_collected)

    # Get all rooms for the filter dropdown
    rooms = Room.objects.all().order_by('room_number')

    context = {
        'rows': rows,
        'total_amount': total_amount,
        'rooms': rooms,
        # Pass back filter values to keep them in the form
        'filter_room': int(room_id) if room_id else '',
        'filter_date_from': date_from,
        'filter_date_to': date_to,
        'filter_name': customer_name,
    }
    return render(request, 'Payment_Scheduler/report.html', context)
