from rest_framework import generics
from rest_framework.response import Response

from users.models import User, generate_invite_code
from users.permissions import IsAuthorization
from users.serializers import UserSerializer, UserInviteCodeSerializer
from users.service import get_referral_users, send_authorization_code


class UserAuthorizationView(generics.CreateAPIView):
    """ View for create and authorization users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Получаем введенный телефон
        phone = request.data['phone']
        validated_phone = UserSerializer(data={'phone': phone})
        if validated_phone.is_valid():
            # Получаем код, если он введён
            input_code = request.data.get('authorization_code')
            if input_code:
                # Если находим поль-ля с таким кодом, то активируем его
                user = User.objects.get(phone=phone)
                user.is_active = True
                user.authorization_code = None
                user.save()
                return Response({'status': 'Accepted', 'status_code': '202', 'result': 'Вы авторизованы!',
                                 'data': {'user_phone': str(user.phone),
                                          'is_active': str(user.is_active),
                                          'invite_code': str(user.personal_invite_code)
                                          }
                                 })
            else:
                # Если код не введён, то генерируем его
                authorization_code_for_user = User.generate_authorization_code()
                # Ищем пользователя по введенному телефону
                if User.objects.filter(phone=phone).first():
                    user = User.objects.filter(phone=phone).first()
                    # Присваиваем сгенерированный код
                    user.authorization_code = authorization_code_for_user
                    user.save()
                    # Имитируем отправку кода авторизации с сервера
                    send_authorization_code(authorization_code_for_user)
                    return Response({'status': 'Accepted', 'code': '202',
                                     'result': 'Введите код авторизации при повторной отправке формы!'})
                else:
                    # Если пользователь не найден, то создаем его
                    User.objects.create(
                        phone=phone,
                        authorization_code=authorization_code_for_user,
                        personal_invite_code=generate_invite_code()
                    )
                    send_authorization_code(authorization_code_for_user)
                    return Response({'status': 'Created', 'code': '201', 'result': 'Пользователь создан. '
                                                                                   f'Но нужно авторизоваться, введите код: '
                                                                                   f'{authorization_code_for_user} при повторной отправке формы!'})
        else:
            return Response({'status': 'Bad request', 'code': '404', 'result': 'Введён невалидный телефон!'})


class UserProfileView(generics.RetrieveAPIView):
    """View for receiving profile data"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthorization, ]

    def retrieve(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if not phone:
            phone = request.query_params.get('phone')
        user = User.objects.filter(phone=phone).first()
        if user:
            list_referral_users = get_referral_users(user.personal_invite_code)
            return Response({'result': 'Ваш профиль:',
                             'profile_data': {
                                 'phone': str(user.phone),
                                 'activation_status': user.is_active,
                                 'personal_invite_code': str(user.personal_invite_code),
                                 'someone_invite_code': str(user.someone_invite_code),
                                 'referral_users': list_referral_users
                             }})
        else:
            return Response({'result': 'Профиль не найден!'})


class UserInputInviteCodeView(generics.UpdateAPIView):
    """View for input and check someone invite code"""
    queryset = User.objects.all()
    serializer_class = UserInviteCodeSerializer
    permission_classes = [IsAuthorization, ]

    def update(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        # Находим пользователя по введенному телефону
        user = User.objects.filter(phone=phone).first()
        # Получаем введённый инвайт-код
        input_invite_code = request.data.get('someone_invite_code')
        # Если инвайт-код есть, то проверяем его на существование
        if User.objects.filter(personal_invite_code=input_invite_code).first():
            # Проверяем у пользователя введённый ранее инвайт-код
            if user.someone_invite_code is None:
                user.someone_invite_code = input_invite_code
                user.save()
                return Response({'result': 'Инвайт-код принят!'})
            else:
                return Response({'result': f'Вы уже вводили инвайт-код: {user.someone_invite_code}'})
        else:
            return Response({'result': 'Инвайт-код  не найден!'})
