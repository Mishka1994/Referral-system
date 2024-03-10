from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None

    phone = PhoneNumberField(region='RU', verbose_name='Телефон', unique=True)
    is_active = models.BooleanField(default=False, verbose_name='Признак активности')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []