from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load all fixtures from fixtures directory in proper order'

    def handle(self, *args, **options):
        # Определяем порядок загрузки фикстур
        fixture_order = [
            'users_fixture.json',
            'courses_fixture.json',
            'lessons_fixture.json',
            'payments_fixture.json'
        ]

        fixtures_path = 'fixtures/'
        loaded_count = 0

        for fixture in fixture_order:
            fixture_path = os.path.join(fixtures_path, fixture)
            if os.path.exists(fixture_path):
                try:
                    call_command('loaddata', fixture_path)
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
                    loaded_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error loading {fixture}: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Fixture {fixture} not found, skipping'))

        self.stdout.write(self.style.SUCCESS(f'Loaded {loaded_count} fixtures'))