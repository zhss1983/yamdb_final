import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_YAMDB

from .models import Code, User


class YAMDBTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределяет стандартное поведение
    сериализатора при получении токкена.
    """

    def __init__(self, *args, **kwargs):
        """
        Удаляем поле 'password' из родительского
        класса, чтобы токен можно было получить
        без пароля в запросе.
        """
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields["password"]

    # Добавляем новое обязательное поле
    confirmation_code = serializers.CharField(max_length=36, required=True)

    def validate(self, attrs):
        """Проверяет confirmation_code."""
        username = attrs["username"]
        user = get_object_or_404(User, username=username)
        if attrs["confirmation_code"] != user.code.code:
            raise serializers.ValidationError("Неверный код подтверждения")
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Имя не может быть me")
        return value

    def create(self, validated_data):
        """
        Тестовая функция записывает тестовый код
        и дату его создания в БД.
        """
        username = validated_data["username"]
        email = validated_data["email"]
        c_code = uuid.uuid4()
        user, _ = User.objects.get_or_create(username=username, email=email)
        Code.objects.get_or_create(user_id=user.id, code=c_code)
        send_mail(
            recipient_list=(user.email,),
            from_email=EMAIL_YAMDB,
            subject="Авторизация на нашем сайте",
            message=f"Ваш код для авторизации {c_code}",
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    lookup_field = "username"

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
