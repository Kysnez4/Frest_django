from django.core.management.base import BaseCommand
from materials.models import Course, Lesson, Payment
from users.models import User
from decimal import Decimal

class Command(BaseCommand):
    help = 'Load test payment data'

    def handle(self, *args, **options):
        # Создаем тестового пользователя
        user, _ = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'phone': '1234567890',
                'country': 'Test Country'
            }
        )

        # Создаем тестовый курс
        course = Course.objects.create(
            name='Test Course',
            preview='course_preview/test.jpg',
            description='Test Description'
        )

        # Создаем тестовый урок
        lesson = Lesson.objects.create(
            course=course,
            name='Test Lesson',
            description='Test Lesson Description',
            preview='lesson_preview/test.jpg',
            video_url='https://example.com/test'
        )

        # Создаем платежи
        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=Decimal('100.00'),
            payment_method='transfer'
        )

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=Decimal('50.00'),
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data'))