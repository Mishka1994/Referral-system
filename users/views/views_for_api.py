from rest_framework import generics
from rest_framework.response import Response

from users.models import User
from users.permissions import IsAuthorization
from users.serializers import UserSerializer, UserProfileSerializer
from users.service import generate_invite_code, generate_authorization_code, get_referral_users


class UserAuthorizationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Получаем введенный телефон
        phone = request.data['phone']
        # Получаем код, если он введён
        input_code = request.data.get('authorization_code')
        if input_code:
            # Если находим поль-ля с таким кодом, то активируем его
            user = User.objects.get(phone=phone)
            user.is_active = True
            user.authorization_code = None
            user.save()
            return Response({'result': 'Вы авторизованы!',
                             'data': {'user_phone': str(user.phone),
                                      'is_active': str(user.is_active),
                                      'invite_code': str(user.personal_invite_code)
                                      }
                             })
        else:
            # Если код не введён, то генерируем его
            authorization_code_for_user = generate_authorization_code()
            # Ищем пользователя по введенному телефону
            if User.objects.filter(phone=phone).first():
                user = User.objects.filter(phone=phone).first()
                # Присваиваем сгенерированный код
                user.authorization_code = authorization_code_for_user
                print(authorization_code_for_user)
                user.save()
                return Response({'result': f'Введите код: {authorization_code_for_user} при повторной отправке формы'})
            else:
                # Если пользователь не найден, то создаем его
                User.objects.create(
                    phone=phone,
                    authorization_code=authorization_code_for_user,
                    personal_invite_code=generate_invite_code()
                )
                print(authorization_code_for_user)
                return Response({'result': 'Пользователь создан. '
                                           f'Но нужно авторизоваться, введите код: {authorization_code_for_user} при повторной отправке формы!'})


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthorization, ]

    def retrieve(self, request, *args, **kwargs):
        # Получаем введённый телефон
        data_with_phone = request.data.get('phone')
        # Находим пользователя по телефону
        user = User.objects.get(phone=data_with_phone)
        # Проверяем введённый инвайт-код
        someone_code = request.data.get('someone_invite_code')
        if someone_code:
            # Если инвайт-код есть, то проверяем его на существование
            if User.objects.filter(personal_invite_code=someone_code).first():
                # Проверяем не вводил ли пользователь ранее инвайт-код
                if user.someone_invite_code is None:
                    user.someone_invite_code = someone_code
                    user.save()
                    return Response({'result': 'Инвайт-код принят!'})
                else:
                    return Response({'result': f'Вы уже вводили ранее чужой инвайт-код: {user.someone_invite_code}'})
            else:
                return Response({'result': 'Инвайт-код не существует!'})
        # Формируем список реферальных поль-ей для информ-ии профиля
        list_users = get_referral_users(user.personal_invite_code)
        # Если инвайт-кода нет в запросе, то возвращаем информацию по профилю пользователя
        return Response({'result': 'Ваш профиль:',
                         'profile_data': {
                             'phone': str(user.phone),
                             'activation_status': user.is_active,
                             'personal_invite_code': str(user.personal_invite_code),
                             'someone_invite_code': str(user.someone_invite_code),
                             'referral_users': list_users
                         }})
