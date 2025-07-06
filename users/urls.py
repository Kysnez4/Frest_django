from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserProfileAPIView, PaymentViewSet, UserCreateAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile-detail'),
    path('payments/', PaymentViewSet.as_view({'get': 'list'}, permission_classes=(AllowAny,)), name='payment-list'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token-refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
]
