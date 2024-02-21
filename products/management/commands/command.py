from django.core.management.base import BaseCommand
from products.models import Sku
from django.db import models

class Command(BaseCommand):
    help = 'Updates existing SKU records'

    def handle(self, *args, **kwargs):
        Sku.objects.update(platform_commission=models.F('selling_price') * 0.25)
        Sku.objects.update(cost_price=models.F('selling_price') - models.F('platform_commission'))
        self.stdout.write(self.style.SUCCESS('Successfully updated SKU records'))
