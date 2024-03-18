from django.urls import path

from users.apps import UsersConfig
from users.views.views_for_django import UserRegisterPhoneView, BaseTemplateView, UserActivateView
from users.views.views_for_api import UserAuthorizationView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    # Urls for Django
    path('', BaseTemplateView.as_view(), name='index'),
    path('create_user/', UserRegisterPhoneView.as_view(), name='create_user'),
    path('authorization_user/', UserActivateView.as_view(), name='activate_user'),

    # Urls for DjangoRESTFramework
    path('api/create/', UserAuthorizationView.as_view(), name='user-create'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile')


]
