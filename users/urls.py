from django.urls import path
from users.views import UserProfileAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
