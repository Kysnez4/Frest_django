from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from materials.models import Lesson, Course
from users.models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name',  'phone', 'country', 'avatar']



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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token['phone'] = user.phone
        token['email'] = user.email

        return token
