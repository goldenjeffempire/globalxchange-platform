# globalxchange/management/commands/my_custom_command.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'This is a custom management command example.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Successfully executed custom command'))
