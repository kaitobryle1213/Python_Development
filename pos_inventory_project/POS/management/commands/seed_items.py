from django.core.management.base import BaseCommand
from django.db import transaction
from POS.models import Item
from decimal import Decimal
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50)

    def handle(self, *args, **options):
        count = options['count']
        created = 0
        with transaction.atomic():
            units = [u[0] for u in Item.UNIT_CHOICES]
            for i in range(1, count + 1):
                code = f"ITEM{i:03d}"
                if Item.objects.filter(item_code=code).exists():
                    continue
                uom = random.choice(units)
                cost = Decimal(random.uniform(10, 500)).quantize(Decimal('0.01'))
                price = (cost * Decimal(random.uniform(1.1, 1.6))).quantize(Decimal('0.01'))
                qty = random.randint(0, 100)
                Item.objects.create(
                    item_code=code,
                    item_description=f"Test Item {i}",
                    unit_of_measure=uom,
                    unit_cost=cost,
                    unit_selling_price=price,
                    quantity_on_hand=qty,
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} items"))
