from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Customer, Payment, BoardingHouseUser
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class TransferCustomerTest(TestCase):
    def setUp(self):
        # Create Admin User
        self.user = BoardingHouseUser.objects.create_superuser(username='admin', password='password', role='Admin')
        self.client = Client()
        self.client.login(username='admin', password='password')

        # Create Rooms
        self.room_cheap = Room.objects.create(
            room_number='101', 
            room_type='Bed Spacer', 
            price=Decimal('1000.00'), 
            capacity=2,
            status='Available'
        )
        self.room_expensive = Room.objects.create(
            room_number='202', 
            room_type='Single', 
            price=Decimal('1500.00'), 
            capacity=1,
            status='Available'
        )
        self.room_vacant = Room.objects.create(
            room_number='303', 
            room_type='Single', 
            price=Decimal('1500.00'), 
            capacity=1,
            status='Available'
        )

        # Create Customer
        self.customer = Customer.objects.create(
            name='John Doe',
            room=self.room_cheap,
            due_date=timezone.localdate(),
            status='Active'
        )

    def test_transfer_upgrade_adjustment(self):
        # Customer pays for the cheap room
        Payment.objects.create(
            customer=self.customer,
            due_date=self.customer.due_date,
            amount=self.room_cheap.price,
            amount_received=self.room_cheap.price,
            is_paid=True
        )

        # Transfer to expensive room
        response = self.client.post(reverse('transfer_customer', args=[self.customer.pk]), {
            'new_room': self.room_expensive.pk
        })
        
        self.assertEqual(response.status_code, 302) # Redirect
        
        # Reload customer
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.room, self.room_expensive)

        # Check for adjustment payment
        payments = Payment.objects.filter(customer=self.customer, due_date=self.customer.due_date)
        total_paid = sum(p.amount_received for p in payments)
        self.assertEqual(total_paid, self.room_expensive.price)
        
        adjustment = payments.filter(remarks__startswith="Transfer Adjustment").first()
        self.assertIsNotNone(adjustment)
        self.assertEqual(adjustment.amount_received, Decimal('500.00'))

    def test_transfer_downgrade_credit(self):
        # Setup: Customer in expensive room, fully paid
        self.customer.room = self.room_expensive
        self.customer.save()
        
        Payment.objects.create(
            customer=self.customer,
            due_date=self.customer.due_date,
            amount=self.room_expensive.price,
            amount_received=self.room_expensive.price,
            is_paid=True
        )

        # Transfer to cheap room
        response = self.client.post(reverse('transfer_customer', args=[self.customer.pk]), {
            'new_room': self.room_cheap.pk
        })

        self.assertEqual(response.status_code, 302)
        
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.room, self.room_cheap)

        # Check for credit payment in NEXT month
        from dateutil.relativedelta import relativedelta
        next_due = self.customer.due_date + relativedelta(months=1)
        
        credit_payment = Payment.objects.filter(customer=self.customer, due_date=next_due).first()
        self.assertIsNotNone(credit_payment)
        self.assertEqual(credit_payment.amount_received, Decimal('500.00'))
        self.assertTrue(credit_payment.remarks.startswith("Transfer Credit"))
        
        # Ensure current cycle is still considered fully paid (balance 0)
        # Note: balance logic is in the view, but we can check the data
        current_payments = Payment.objects.filter(customer=self.customer, due_date=self.customer.due_date)
        total_paid_current = sum(p.amount_received for p in current_payments)
        # Total paid is still 1500, price is 1000. Balance is 0.
        self.assertEqual(total_paid_current, Decimal('1500.00'))
