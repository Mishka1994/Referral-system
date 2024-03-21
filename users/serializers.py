from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region='RU')

    class Meta:
        model = User
        fields = ['phone', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'is_active', 'personal_invite_code', 'someone_invite_code']
