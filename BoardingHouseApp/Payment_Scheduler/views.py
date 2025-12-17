from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Payment, BoardingHouseUser
from .forms import CustomerForm, BoardingHouseUserForm, BoardingHouseUserEditForm
from datetime import date, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

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

@login_required
def dashboard_view(request):
    payments = Payment.objects.all().select_related('customer')
    today = timezone.now().date()
    
    payment_data = []
    for payment in payments:
        color = 'white' # Default for paid?
        # Logic:
        # Paid -> White
        # 5 days before due -> Yellow
        # Due date -> Red
        # Overdue -> Black
        
        days_until_due = (payment.due_date - today).days
        
        if payment.is_paid:
            color = 'white'
        elif days_until_due < 0:
            color = 'black'
        elif days_until_due == 0:
            color = 'red'
        elif days_until_due <= 5:
            color = 'yellow'
        else:
            color = 'green' # Default for safe? Or maybe just no color/default. User didn't specify. I'll use green or transparent.
            
        payment_data.append({
            'payment': payment,
            'color': color
        })
        
    return render(request, 'Payment_Scheduler/dashboard.html', {'payment_data': payment_data})

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

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def payment_view(request):
    return render(request, 'Payment_Scheduler/payment.html')

@login_required
def search_customers(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | Q(room_no__icontains=query)
        )[:10]  # Limit to 10 results
        results = []
        for c in customers:
            # Calculate total balance
            balance = sum(p.amount for p in c.payments.filter(is_paid=False))
            results.append({
                'id': c.customer_id,
                'name': c.name,
                'room_no': c.room_no,
                'balance': balance
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def get_customer_balance(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    # Find the earliest unpaid payment
    payment = Payment.objects.filter(customer=customer, is_paid=False).order_by('due_date').first()
    
    if payment:
        return JsonResponse({
            'customer_id': customer.customer_id,
            'name': customer.name,
            'room_no': customer.room_no,
            'payment_id': payment.id,
            'due_date': payment.due_date,
            'balance': payment.amount,
        })
    else:
        # If no unpaid payment, we can create one or just return empty
        # For now, let's assume we can't pay if there's no bill
        return JsonResponse({'error': 'No pending payments for this customer.'})

@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        amount_received = request.POST.get('amount_received')
        change_amount = request.POST.get('change_amount')
        
        try:
            payment = Payment.objects.get(pk=payment_id)
            payment.amount_received = amount_received
            payment.change_amount = change_amount
            payment.date_paid = timezone.now().date()
            payment.is_paid = True
            payment.save()
            return JsonResponse({'success': True})
        except Payment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Payment record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
