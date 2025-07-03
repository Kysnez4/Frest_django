from rest_framework import serializers

from materials.models import Lesson, Course
from users.models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'country', 'avatar']
        read_only_fields = ['email']

class PaymentSerializer(serializers.ModelSerializer):
    paid_course = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Course.objects.all(),
        required=False,
        allow_null=True
    )
    paid_lesson = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Lesson.objects.all(),
        required=False,
        allow_null=True
    )
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )

    class Meta:
        model = Payment
        fields = '__all__'