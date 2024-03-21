from django.urls import path

from users.apps import UsersConfig
from users.views.views_for_dj_templates import UserRegisterPhoneView, BaseTemplateView, authorization_view
from users.views.views_for_api import UserAuthorizationView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    # Urls for Django Templates
    path('', BaseTemplateView.as_view(), name='index'),
    path('create_user/', UserRegisterPhoneView.as_view(), name='create_user'),
    path('authorization_user/', authorization_view, name='activate_user'),

    # Urls for DjangoRESTFramework
    path('api/create/', UserAuthorizationView.as_view(), name='user-create'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile')

]
