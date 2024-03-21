import secrets
import string
import time
import random

def generate_authorization_code():
    time.sleep(3)
    authorization_code = str()
    for _ in range(4):
        authorization_code += str(random.randint(0, 9))
    return authorization_code


def generate_invite_code():
    letters_and_digits = string.ascii_letters + string.digits
    invite_code = ''.join(secrets.choice(
        letters_and_digits) for i in range(6))
    return invite_code
