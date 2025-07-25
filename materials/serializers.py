from rest_framework import serializers
from materials.models import Course, Lesson, Subscribe
from materials.validators import ExternalLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'description': {'validators': [ExternalLinkValidator()]},
            'owner': {'read_only': True},
        }

    def validate_video_url(self, value):
        """Проверяем, что ссылка ведет на YouTube"""
        if 'youtube.com' not in value.lower() and 'youtu.be' not in value.lower():
            raise serializers.ValidationError("Разрешены только ссылки на YouTube")
        return value


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons',
                  'lessons_count', 'is_subscribed']
        extra_kwargs = {
            'description': {'validators': [ExternalLinkValidator()]},
        }

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(user=request.user).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['id', 'user', 'course', 'created_at']


class CourseDetailSerializer(CourseSerializer):
    subscription = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['subscription']

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            subscription = obj.subscribers.filter(user=request.user).first()
            if subscription:
                return SubscriptionSerializer(subscription).data
        return None
