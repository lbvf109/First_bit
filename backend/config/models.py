from django.core.validators import RegexValidator
from django.db import models


class Registration(models.Model):
    parent_name = models.CharField('Имя', max_length=150)
    baby_name = models.CharField('Имя малыша', max_length=150)
    phone = models.CharField(
        'Телефон', max_length=20, unique=True,
        validators=[RegexValidator(
            r'^\+?[0-9\s\-()]{10,20}$', 'Введите корректный номер телефона.')],
        error_messages={'unique': 'Этот телефон уже зарегистрирован.'},
    )
    baby_birth_date = models.DateField('Дата рождения ребенка')
    created_at = models.DateTimeField(auto_now_add=True)
