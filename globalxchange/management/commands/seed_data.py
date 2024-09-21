# globalxchange/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from globalxchange.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Create sample product
        Product.objects.create(name='Sample Product', description='This is a sample product.', price=100.00)
        self.stdout.write(self.style.SUCCESS('Database seeded with initial data'))
