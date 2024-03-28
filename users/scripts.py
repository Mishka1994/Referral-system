import secrets
import string


def generate_invite_code():
    """ Функция для формирования личного инвайт-кода """
    letters_and_digits = string.ascii_letters + string.digits
    invite_code = ''.join(secrets.choice(
        letters_and_digits) for _ in range(6))
    return invite_code
