# не знаю зачем я это перенес :D
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email",
            }
        )
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите номер телефона",
            }
        ),
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите город",
            }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Подтвердите пароль",
            }
        )
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if phone and not phone.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        return phone
