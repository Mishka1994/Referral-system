import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.scripts import generate_invite_code

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    phone = PhoneNumberField(region='RU', verbose_name='Телефон', unique=True)
    authorization_code = models.CharField(max_length=4, verbose_name='Код активации', default=None, **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Признак активности')
    personal_invite_code = models.CharField(max_length=6, verbose_name='Персональный инвайт-код',
                                            default=generate_invite_code())
    someone_invite_code = models.CharField(max_length=6, verbose_name='Чужой инвайт-код', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone}'

    @staticmethod
    def generate_authorization_code():
        """ Функция для формирования кода авторизации """
        digits = string.digits
        authorization_code = ''.join(secrets.choice(digits) for _ in range(4))
        return authorization_code
