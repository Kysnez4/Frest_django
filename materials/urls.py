from rest_framework.routers import DefaultRouter
from django.urls import path, include
from materials.views import (CourseViewSet,
                             LessonLCAPIView,
                             LessonRUDAPIView)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonLCAPIView.as_view(), name='lesson-lc'),
    path('lessons/<int:pk>/', LessonRUDAPIView.as_view(), name='lesson-rud'),
]