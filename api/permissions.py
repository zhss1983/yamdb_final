from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)

from api.users.constants import ADMIN, MODERATOR


class EditAccessOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Объект уровня доступа. Доступ только для автора, модератора и выше.
    """
    FULL_ACCESS = (MODERATOR, ADMIN)

    def has_object_permission(self, request, view, obj):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        author = auth and obj.author == request.user
        admin = auth and (
            request.user.is_superuser or request.user.role in self.FULL_ACCESS)
        return safe or author or admin


class AdminOrReadOnly(BasePermission):
    """
    Объект уровня доступа. Доступ только для автора и администратора.
    """

    def has_permission(self, request, view):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        admin = auth and (request.user.is_superuser
                          or request.user.role == ADMIN)
        return safe or admin
