from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterPhoneView, BaseTemplateView, AuthorizationTemplateView

app_name = UsersConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='index'),
    path('create_user/', UserRegisterPhoneView.as_view(), name='create_user'),
    path('authorization/', AuthorizationTemplateView.as_view(), name='activate_user')


]
