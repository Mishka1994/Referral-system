from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    phone = PhoneNumberField(region='RU', verbose_name='Телефон', unique=True)
    authorization_code = models.PositiveSmallIntegerField(verbose_name='Код активации', default=None, blank=True,
                                                          null=True)
    is_active = models.BooleanField(default=False, verbose_name='Признак активности')
    personal_invite_code = models.CharField(max_length=6, verbose_name='Персональный инвайт-код', **NULLABLE)
    someone_invite_code = models.CharField(max_length=6, verbose_name='Чужой инвайт-код', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
