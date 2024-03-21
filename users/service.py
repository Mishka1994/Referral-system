import secrets
import string
import time
import random

from users.models import User


def get_referral_users(code):
    """ Функция для формирования списка поль-ей, которые использовали инвайт-код данного пользователя"""
    users = User.objects.filter(someone_invite_code=code)
    list_users = [str(user) for user in users]
    return list_users

def generate_authorization_code():
    """ Функция для формирования кода авторизации """
    time.sleep(3)
    authorization_code = str()
    for _ in range(4):
        authorization_code += str(random.randint(0, 9))
    return authorization_code


def generate_invite_code():
    """ Функция для формирования личного инвайт-кода """
    letters_and_digits = string.ascii_letters + string.digits
    invite_code = ''.join(secrets.choice(
        letters_and_digits) for i in range(6))
    return invite_code
