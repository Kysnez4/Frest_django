from rest_framework import serializers

from materials.models import Lesson, Course
from users.models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'country', 'avatar']


class PublicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'phone', 'country', 'avatar']
        read_only_fields = fields  # Все поля только для чтения


class PrivateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'country', 'avatar', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'last_name': {'write_only': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)


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
