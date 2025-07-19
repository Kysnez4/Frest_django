from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from users.permission import IsOwner
from users.models import User, Payment
from users.serializers import (PaymentSerializer,
                               PrivateUserProfileSerializer,
                               PublicUserProfileSerializer,
                               UserProfileSerializer)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PrivateUserProfileSerializer  # Базовый сериализатор для PUT/PATCH

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user == self.get_object():
                return PrivateUserProfileSerializer
            return PublicUserProfileSerializer
        return PrivateUserProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            return generics.get_object_or_404(User, pk=user_id)
        return self.request.user


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        'paid_course': ['exact'],
        'paid_lesson': ['exact'],
        'payment_method': ['exact'],
    }
    ordering_fields = ['date', 'amount']
    search_fields = ['user__email', 'paid_course__name', 'paid_lesson__name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)