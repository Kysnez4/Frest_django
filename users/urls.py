from django.urls import path
from users.views import UserProfileAPIView, PaymentViewSet

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('payments/', PaymentViewSet.as_view({'get': 'list'}), name='payment-list'),
]
