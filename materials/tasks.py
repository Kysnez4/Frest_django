from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscribe


@shared_task
def send_course_update_notification(course_id):
    """
    Отправляет уведомления подписчикам курса об обновлении
    """
    course = Course.objects.get(id=course_id)
    subscribers = Subscribe.objects.filter(course=course).select_related('user')

    subject = f'Обновление материалов курса "{course.name}"'
    message = f'Материалы курса "{course.name}" были обновлены. Проверьте новые материалы!'

    for subscription in subscribers:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )