from django.urls import path

from users.apps import UsersConfig
from users.views.views_for_django import UserRegisterPhoneView, BaseTemplateView, AuthorizationTemplateView
from users.views.views_for_api import UserAuthorizationView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    # Urls for Django
    path('', BaseTemplateView.as_view(), name='index'),
    path('create_user/', UserRegisterPhoneView.as_view(), name='create_user'),
    path('authorization/', AuthorizationTemplateView.as_view(), name='activate_user'),

    # Urls for DjangoRESTFramework
    path('create/', UserAuthorizationView.as_view(), name='user-create'),
    path('list/', UserListView.as_view(), name='user-list'),


]
