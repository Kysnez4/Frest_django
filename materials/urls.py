from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from materials.views import CourseViewSet, LessonLCAPIView, LessonRUDAPIView, SubscribeAPIView

app_name = "materials"
router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonLCAPIView.as_view(permission_classes=(AllowAny,)), name='lesson-lc'),
    path('lessons/<int:pk>/', LessonRUDAPIView.as_view(permission_classes=(AllowAny,)), name='lesson-rud'),
    path('courses/<int:course_id>/subscribe/', SubscribeAPIView.as_view(), name='subscribe'),

]
