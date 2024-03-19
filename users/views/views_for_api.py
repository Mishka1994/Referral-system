from rest_framework import generics
from rest_framework.response import Response

from users.models import User
from users.permissions import IsAuthorization
from users.serializers import UserSerializer, UserProfileSerializer
from users.service import generate_invite_code
from users.tasks import generate_authorization_code


class UserAuthorizationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [IsAuthorization,]

    def create(self, request, *args, **kwargs):
        phone = request.data['phone']
        input_code = request.data.get('authorization_code')
        if input_code:
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
            result = generate_authorization_code.delay()
            code = result.get()
            if User.objects.filter(phone=phone).first():
                user = User.objects.filter(phone=phone).first()
                user.authorization_code = code
                print(code)
                user.save()
                return Response({'result': f'Введите код: {code} при повторной отправке формы'})
            else:
                User.objects.create(
                    phone=phone,
                    authorization_code=code,
                    personal_invite_code=generate_invite_code()
                )
                print(code)
                return Response({'result': 'Пользователь создан. '
                                           f'Но нужно авторизоваться, введите код: {code} при повторной отправке формы!'})


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer()
    permission_classes = [IsAuthorization, ]

    def retrieve(self, request, *args, **kwargs):
        data_with_phone = request.data.get('phone')
        user = User.objects.get(phone=data_with_phone)
        someone_code = request.data.get('someone_invite_code')
        if someone_code:
            if User.objects.get(personal_invite_code=someone_code):
                if user.someone_invite_code is None:
                    user.someone_invite_code = someone_code
                    user.save()
                    return Response({'result': 'Инвайт-код принят!'})
                else:
                    return Response({'result': f'Вы уже вводили ранее чужой инвайт-код: {user.someone_invite_code}'})
            else:
                return Response({'result': 'Инвайт-код не существует!'})
        return Response({'result': 'Ваш профиль:',
                         'profile_data': {
                             'phone': str(user.phone),
                             'activation_status': user.is_active,
                             'personal_invite_code': str(user.personal_invite_code),
                             'someone_invite_code': str(user.someone_invite_code),
                             'users_your_invite_code': self.serializer_class.get_users_your_code(user)
                         }})
