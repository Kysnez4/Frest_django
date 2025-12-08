from datetime import timedelta

from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from django.utils import timezone

from materials.models import Course, Lesson, Subscribe
from materials.paginators import CoursePagination
from materials.tasks import send_course_update_notification
from users.permission import IsModer, IsOwner
from users.serializers import PaymentSerializer
from users.services.stripe_service import create_stripe_session, create_stripe_product, create_stripe_price
from materials.serializers import (CourseSerializer,
                                   LessonSerializer,
                                   SubscriptionSerializer,
                                   CourseDetailSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if timezone.now() - instance.last_update > timedelta(hours=4):
            send_course_update_notification.delay(instance.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer


class LessonLCAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (~IsModer,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "GET"]:
            self.permission_classes = (IsModer | IsOwner,)
        else:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.course.last_update = timezone.now()
        instance.course.save()

        # Проверяем, нужно ли отправлять уведомление
        if timezone.now() - instance.course.last_update > timedelta(hours=4):
            send_course_update_notification.delay(instance.course.id)


class SubscribeAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'course_id'

    def get_queryset(self):
        return Subscribe.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        if self.get_queryset().filter(course=course).exists():
            raise ValidationError("You are already subscribed to this course.")
        serializer.save(user=self.request.user, course=course)

    def delete(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_id')
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # Создаем продукт в Stripe
        product = create_stripe_product(payment)
        payment.stripe_product_id = product.id

        # Создаем цену в Stripe
        price = create_stripe_price(payment, product.id)
        payment.stripe_price_id = price.id

        # Создаем сессию оплаты
        success_url = self.request.build_absolute_uri(
            reverse('payment-success')
        )
        cancel_url = self.request.build_absolute_uri(
            reverse('payment-cancel')
        )

        session = create_stripe_session(
            price.id,
            success_url,
            cancel_url
        )

        payment.stripe_session_id = session.id
        payment.stripe_payment_link = session.url
        payment.save()


class PaymentSuccessAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "Payment successful"}, status=status.HTTP_200_OK)


class PaymentCancelAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "Payment cancelled"}, status=status.HTTP_200_OK)
