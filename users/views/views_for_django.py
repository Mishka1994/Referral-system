from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from phonenumber_field.formfields import PhoneNumberField

from users.forms import UserForm
from users.models import User
from users.tasks import generate_authorization_code


class BaseTemplateView(TemplateView):
    template_name = 'users/index.html'


class UserRegisterPhoneView(CreateView):
    model = User
    form_class = UserForm
    # success_url = reverse_lazy('users:activate_user', args=[])

    def form_valid(self, form):
        if form.is_valid():
            code_for_user = generate_authorization_code()
            print(code_for_user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('activate_user', self.object.pk)


class UserActivateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:index')


# class AuthorizationTemplateView(TemplateView):
#     template_name = 'users/user_authorization.html'
#
#     def get(self, request, *args, **kwargs):
#         pass
