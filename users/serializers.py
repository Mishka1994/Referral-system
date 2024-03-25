from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region='RU')

    class Meta:
        model = User
        fields = ('phone', 'authorization_code', 'personal_invite_code', 'someone_invite_code',)


class UserInviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'someone_invite_code',)
