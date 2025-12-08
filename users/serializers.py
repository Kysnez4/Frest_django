from rest_framework import serializers

from materials.models import Lesson, Course, Payment
from users.models import User


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
        queryset=User.objects.all(),
        required=False
    )
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'date', 'stripe_product_id', 'stripe_price_id',
                          'stripe_session_id', 'stripe_payment_link', 'stripe_payment_status']

    def get_payment_link(self, obj):
        return obj.stripe_payment_link

    def validate(self, data):
        if not data.get('paid_course') and not data.get('paid_lesson'):
            raise serializers.ValidationError("Необходимо указать курс или урок для оплаты")
        return data