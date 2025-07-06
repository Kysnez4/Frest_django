from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from users.serializers import UserProfileSerializer, PaymentSerializer, MyTokenObtainPairSerializer
from users.models import User, Payment


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


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
