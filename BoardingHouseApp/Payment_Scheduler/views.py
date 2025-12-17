from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Payment, BoardingHouseUser, Room
from .forms import CustomerForm, BoardingHouseUserForm, BoardingHouseUserEditForm, RoomForm
from datetime import date, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

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
    """
    Logic: Paid (Green) priority. If a payment exists for the current due date, 
    status is Paid. Otherwise, it calculates aging (Overdue, Due Today, etc.).
    """
    customers = Customer.objects.all().select_related('room').prefetch_related('payments')
    today = timezone.now().date()
    payment_data = []
    
    for customer in customers:
        # Check if there is a payment record marked as paid for the CURRENT set due_date
        is_currently_paid = customer.payments.filter(due_date=customer.due_date, is_paid=True).exists()
        
        # Get the very last payment for historical reference
        last_payment_record = customer.payments.filter(is_paid=True).order_by('-date_paid').first()

        if is_currently_paid:
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
            elif days_until_due <= 3: 
                color = 'yellow'
                status_text = "Due Soon"
            else:
                color = 'white'
                status_text = "Upcoming"
        else:
            color = 'white'
            status_text = "No Schedule"
        
        payment_data.append({
            'customer': customer,
            'payment': {
                'amount': customer.room.price if customer.room else 0,
                'previous_date': last_payment_record.date_paid if last_payment_record else "-"
            },
            'color': color,
            'status_text': status_text
        })
        
    return render(request, 'Payment_Scheduler/dashboard.html', {'payment_data': payment_data})


# --- ROOM MANAGEMENT ---

@login_required
def room_view(request):
    rooms = Room.objects.all()
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
    rooms = Room.objects.filter(Q(room_number__icontains=query) & Q(status='Available')) if query else Room.objects.filter(status='Available')
    results = [{'id': r.id, 'room_number': r.room_number, 'room_type': r.room_type, 'status': r.status, 'price': r.price} for r in rooms]
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
            form.save()
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
            form.save()
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
    """
    Fixed search function to ensure 'id' is the database primary key 
    needed for the URL mapping in the frontend.
    """
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | 
            Q(room__room_number__icontains=query) |
            Q(room_no__icontains=query)  # Include legacy room_no search
        )[:10]
        results = []
        for c in customers:
            results.append({
                'id': c.pk,                      # Database PK
                'display_id': c.customer_id,     # ID-001 format
                'name': c.name,
                'room_no': c.room.room_number if c.room else (c.room_no if c.room_no else "N/A"),
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def get_customer_balance(request, customer_id):
    """
    Fixed to handle the database primary key and correctly identify 
    the payment schedule.
    """
    customer = get_object_or_404(Customer, pk=customer_id)
    
    # Try to find a payment record for the current set due_date that is unpaid
    payment = Payment.objects.filter(customer=customer, due_date=customer.due_date, is_paid=False).first()
    
    # Format the due date properly for the HTML input
    if customer.due_date:
        due_date_str = customer.due_date.strftime('%Y-%m-%d')
    else:
        due_date_str = timezone.now().date().strftime('%Y-%m-%d')

    return JsonResponse({
        'customer_id': customer.customer_id, # String ID for display
        'customer_db_id': customer.pk,       # Numeric PK for hidden input
        'name': customer.name,
        'room_no': customer.room.room_number if customer.room else (customer.room_no if customer.room_no else "N/A"),
        'payment_id': payment.id if payment else "", 
        'due_date': due_date_str,
        'balance': customer.room.price if customer.room else 0,
    })

@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        customer_id = request.POST.get('customer_id') 
        amount_received = request.POST.get('amount_received')
        change_amount = request.POST.get('change_amount')
        
        try:
            if payment_id and payment_id.strip() != "":
                payment = Payment.objects.get(pk=payment_id)
            else:
                customer = Customer.objects.get(pk=customer_id)
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
            
            return JsonResponse({'success': True})
            
        except (Payment.DoesNotExist, Customer.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})