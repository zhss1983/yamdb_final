from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ACCESS_LEVEL, ADMIN, USER
from .managers import CustomUserManager


class User(AbstractUser):
    """Кастомная модель пользователя с доплнительными полями 'role' и 'bio'."""

    role = models.CharField(
        verbose_name='Права',
        max_length=9,
        choices=ACCESS_LEVEL,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    email = models.EmailField(unique=True)

    # Необходимо для того, чтобы при создании
    # пользователя через консоль, запрашивался
    # email
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def not_admin(self):
        return self.role != ADMIN

    def __str__(self):
        return self.username


class Code(models.Model):
    """Модель для хранения confirmation code
    пользователя.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='code',
        verbose_name='Пользователь',
        primary_key=True
    )
    code = models.CharField(
        max_length=36,
        verbose_name='confirmation_code'
    )

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
