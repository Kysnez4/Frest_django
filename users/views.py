from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from users.serializers import UserProfileSerializer, PaymentSerializer
from users.models import User, Payment


# Create your views here.


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Возвращаем текущего пользователя


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Возвращаем текущего пользователя


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        'paid_course': ['exact'],
        'paid_lesson': ['exact'],
        'payment_method': ['exact'],
    }
    ordering_fields = ['date', 'amount']
    search_fields = ['user__email', 'paid_course__name', 'paid_lesson__name']
    permission_classes = [IsAuthenticated]  # Добавляем проверку аутентификации

    def get_queryset(self):
        # По умолчанию показываем только платежи текущего пользователя
        return self.queryset.filter(user=self.request.user)
