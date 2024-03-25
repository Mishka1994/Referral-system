import time

from users.models import User


def get_referral_users(code):
    """ Функция для формирования списка поль-ей, которые использовали инвайт-код данного пользователя"""
    users = User.objects.filter(someone_invite_code=code)
    list_users = [str(user) for user in users]
    return list_users


def send_authorization_code(code):
    """Функция для имитации отправки кода авторизации с сервиса"""
    time.sleep(3)
    return code
