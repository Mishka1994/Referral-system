from django import forms
from phonenumber_field.formfields import PhoneNumberField

from users.models import User


# class DesignFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone',)


class PhoneForm(forms.Form):
    number = PhoneNumberField(region='RU')
