from django.db import migrations, models

def fix_null_customer_id(apps, schema_editor):
    Customer = apps.get_model('Payment_Scheduler', 'Customer')
    
    # Find customers with null customer_id
    null_customers = Customer.objects.filter(customer_id__isnull=True)
    
    if null_customers.exists():
        # Get the maximum customer_id to determine the next value
        max_id_result = Customer.objects.exclude(customer_id__isnull=True).aggregate(max_id=models.Max('customer_id'))
        max_id = max_id_result['max_id'] or 0
        
        for customer in null_customers:
            max_id += 1
            customer.customer_id = max_id
            customer.save()

def reverse_fix_null_customer_id(apps, schema_editor):
    # This migration cannot be reversed safely
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('Payment_Scheduler', '0014_alter_room_date_created'),
    ]

    operations = [
        migrations.RunPython(fix_null_customer_id, reverse_fix_null_customer_id),
    ]