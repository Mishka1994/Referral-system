from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from phonenumber_field.formfields import PhoneNumberField

from users.forms import UserForm
from users.models import User
from users.service import generate_authorization_code, generate_invite_code


class BaseTemplateView(TemplateView):
    template_name = 'users/index.html'


class UserRegisterPhoneView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:activate_user', args=[])

    def post(self, request, *args, **kwargs):
        invite_code_for_user = generate_invite_code()
        authorization_code_for_user = generate_authorization_code()
        phone_user = request.POST.get('phone')
        user = User.objects.filter(phone=phone_user)
        if user:
            user.authorization_code = authorization_code_for_user
            user.personal_invite_code = invite_code_for_user
            user.save()
            print(authorization_code_for_user)
        else:
            User.objects.create(
                phone=phone_user,
                authorization_code=authorization_code_for_user,
                personal_invite_code=invite_code_for_user
            )
            print(authorization_code_for_user)

        return HttpResponseRedirect('http://localhost:8000/authorization_user/')


def authorization_view(request):
    data = {}
    if request.method == 'POST':
        input_code = request.POST.get('code')
        user = User.objects.filter(authorization_code=input_code).first()
        if user:
            user.is_active = True
            user.save()
            data['status'] = 'Вы авторизованны!'
            return render(request, 'users/activate_result.html', data)
        else:
            data['status'] = 'Упс, что-то пошло не так!'
            return render(request, 'users/activate_result.html', data)
    return render(request, 'users/user_authorization.html')
