from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from materials.views import CourseViewSet, LessonLCAPIView, LessonRUDAPIView, SubscribeAPIView, PaymentCreateAPIView, \
    PaymentSuccessAPIView, PaymentCancelAPIView

app_name = "materials"
router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonLCAPIView.as_view(permission_classes=(AllowAny,)), name='lesson-lc'),
    path('lessons/<int:pk>/', LessonRUDAPIView.as_view(permission_classes=(AllowAny,)), name='lesson-rud'),
    path('courses/<int:course_id>/subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('payments/cancel/', PaymentCancelAPIView.as_view(), name='payment-cancel'),
]
