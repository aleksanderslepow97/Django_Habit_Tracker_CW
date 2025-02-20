from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле электронной почты должно быть задано")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        **NULLABLE,
        verbose_name="Телефон",
        help_text="Укажите номер телефона"
    )
    avatar = models.ImageField(
        upload_to=r"users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите фото аватара"
    )
    tg_nick = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="ТГ-ник",
        help_text="Укажите телеграмм-ник"
    )
    tg_chat_id = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Телеграмм chat-id",
        help_text="Укажите телеграмм chat-id"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
