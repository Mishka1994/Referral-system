from rest_framework import generics
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer
from users.service import generate_authorization_code


class UserAuthorizationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data['phone']
        input_code = request.data.get('authorization_code')
        if input_code:
            user = User.objects.get(phone=phone)
            user.is_active = True
            user.authorization_code = None
            user.save()
            return Response({'result': 'Вы авторизованы!'})
        else:
            code = generate_authorization_code()
            if User.objects.filter(phone=phone).first():
                user = User.objects.filter(phone=phone).first()
                user.authorization_code = code
                print(code)
                user.save()
                return Response({'result': 'Введите код при повторной отправке формы'})
            else:
                User.objects.create(
                    phone=phone,
                    authorization_code=code
                )
                print(code)
                return Response({'result': 'Пользователь создан. '
                                           'Но нужно авторизоваться, введите код при повторной отправке формы!'})

    # def create_(self, ):
    #     user = serializer.save()
    #     if user.authorization_code:
    #         user = User.objects.filter(phone=user.phone).first()
    #         user.is_active = True
    #         user.authorization_code = None
    #         user.save()
    #     else:
    #         code = generate_authorization_code()
    #         if User.objects.filter(phone=user.phone).first():
    #             user = User.objects.filter(phone=user.phone).first()
    #             user.authorization_code = code
    #             print(code)
    #             user.save()
    #         else:
    #             User.objects.create(
    #                 phone=user,
    #                 authorization_code=code
    #             )
    #             print(code)



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
