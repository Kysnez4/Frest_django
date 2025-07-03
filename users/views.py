from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserProfileSerializer
from users.models import User


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
