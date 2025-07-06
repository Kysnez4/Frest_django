from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load payments data from fixture'

    def handle(self, *args, **options):
        try:
            call_command('loaddata', 'fixtures/payments_fixture.json')
            self.stdout.write(self.style.SUCCESS('Payments data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))