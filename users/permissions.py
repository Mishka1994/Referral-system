from rest_framework.permissions import BasePermission

from users.models import User


class IsAuthorization(BasePermission):

    def has_permission(self, request, view):
        customer = view.queryset.first()
        customer = User.objects.filter(phone=customer.phone).first()
        return customer.is_active
