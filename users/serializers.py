from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region='RU')

    class Meta:
        model = User
        fields = ['phone', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    users_your_code = serializers.SerializerMethodField()

    def get_users_your_code(self, obj):
        users = User.objects.filter(someone_invite_code=obj.personal_invite_code)
        list_users = [str(user) for user in users]
        return list_users

    class Meta:
        model = User
        fields = ['phone', 'is_active', 'personal_invite_code', 'someone_invite_code', 'users_your_code']
