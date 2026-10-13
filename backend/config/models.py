import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


def normalize_phone(raw):
    """Приводит номер к единому виду: '8 (904) 756-38-08' -> '+79047563808'."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits[0] in "78":
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits
    return "+" + digits


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra):
        if not phone:
            raise ValueError("Нужен телефон")
        user = self.model(phone=normalize_phone(phone), **extra)
        user.set_password(password)          # хеширует пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        "Телефон", max_length=20, unique=True,
        error_messages={"unique": "Этот телефон уже зарегистрирован."},
    )
    parent_name = models.CharField("Имя", max_length=150)
    baby_name = models.CharField("Имя малыша", max_length=150, blank=True)
    baby_birth_date = models.DateField(
        "Дата рождения ребенка", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"          # по этому полю входят
    REQUIRED_FIELDS = ["parent_name"]  # что спросит createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.phone
