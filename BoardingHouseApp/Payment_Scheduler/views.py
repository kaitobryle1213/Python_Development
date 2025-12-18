from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Payment, BoardingHouseUser, Room
from .forms import CustomerForm, BoardingHouseUserForm, BoardingHouseUserEditForm, RoomForm
from datetime import date, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Count, F, Sum
from dateutil.relativedelta import relativedelta
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Room

# --- AUTHENTICATION ---

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

@login_required
def search_rooms(request):
    query = request.GET.get('q', '')
    
    # Filter for rooms that are NOT Under Maintenance
    rooms = Room.objects.exclude(status='Under Maintenance').annotate(
        current_occupants=Count('customers', filter=Q(customers__status='Active')),
        safe_capacity=Coalesce(F('capacity'), Value(1))
    ).filter(
        # Room must have at least one empty slot
        current_occupants__lt=F('safe_capacity')
    )

    if query:
        rooms = rooms.filter(room_number__icontains=query)

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
            'available_slots': r.safe_capacity - r.current_occupants
        })
    
    return JsonResponse(results, safe=False)


# --- USER MANAGEMENT ---

@login_required
def user_management_view(request):
    users = BoardingHouseUser.objects.all()
    return render(request, 'Payment_Scheduler/user.html', {'users': users})

@login_required
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
def customer_view(request):
    customers = Customer.objects.all()
    return render(request, 'Payment_Scheduler/customer.html', {'customers': customers})

@login_required
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
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'Payment_Scheduler/customer_detail.html', {'customer': customer})


# --- PAYMENT PROCESSING ---

@login_required
def payment_view(request):
    return render(request, 'Payment_Scheduler/payment.html')

@login_required
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
def get_customer_balance(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    payment = Payment.objects.filter(customer=customer, due_date=customer.due_date, is_paid=False).first()
    
    if customer.due_date:
        due_date_str = customer.due_date.strftime('%Y-%m-%d')
    else:
        due_date_str = timezone.now().date().strftime('%Y-%m-%d')

    return JsonResponse({
        'customer_id': customer.customer_id,
        'customer_db_id': customer.pk,
        'name': customer.name,
        'room_no': customer.room.room_number if customer.room else (customer.room_number if customer.room_number else "N/A"),
        'payment_id': payment.id if payment else "", 
        'due_date': due_date_str,
        'balance': customer.room.price if customer.room else 0,
    })

@login_required
def dashboard_api(request):
    """Returns live dashboard data as JSON for background refreshing."""
    customers = Customer.objects.all().select_related('room').prefetch_related('payments')
    today = timezone.now().date()
    data = []
    
    for customer in customers:
        last_payment = customer.payments.filter(is_paid=True).order_by('-date_paid').first()
        is_paid_today = last_payment and last_payment.date_paid == today

        if is_paid_today:
            color, status = 'green', "Paid"
        elif customer.due_date:
            days = (customer.due_date - today).days
            if days < 0: color, status = 'black', "Overdue"
            elif days == 0: color, status = 'red', "Due Today"
            elif days <= 3: color, status = 'yellow', "Due Soon"
            else: color, status = 'white', "Upcoming"
        else:
            color, status = 'white', "No Schedule"

        data.append({
            'name': customer.name,
            'room_no': customer.room.room_number if customer.room else (customer.room_no or "-"),
            'prev_payment': last_payment.date_paid.strftime('%b %d, %Y') if last_payment else "-",
            'due_date': customer.due_date.strftime('%b %d, %Y') if customer.due_date else "N/A",
            'amount': f"₱{customer.room.price}" if customer.room else "-",
            'status': status,
            'color': color
        })
    return JsonResponse({'payment_data': data})

@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        customer_id = request.POST.get('customer_id') 
        amount_received = request.POST.get('amount_received')
        change_amount = request.POST.get('change_amount')
        
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

            payment.amount_received = amount_received
            payment.change_amount = change_amount
            payment.date_paid = timezone.now().date()
            payment.is_paid = True
            payment.save()
            
            # --- ADVANCE DUE DATE BY 1 MONTH ---
            if customer.due_date:
                customer.due_date = customer.due_date + relativedelta(months=1)
                customer.save()
            
            return JsonResponse({'success': True})
            
        except (Payment.DoesNotExist, Customer.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
