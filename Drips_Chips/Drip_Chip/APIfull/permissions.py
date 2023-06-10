from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
        )

class IsNotAuthentications(BasePermission):

    def has_permission(self, request, view):
        if request.user:
            raise PermissionDenied('Регистрация разрешена только неавторизованным пользователям')
        else:
            return True