import random


def generate_authorization_code():
    authorization_code = str()
    for _ in range(4):
        authorization_code += str(random.randint(0, 9))
    return authorization_code
