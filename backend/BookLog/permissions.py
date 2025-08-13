# permissions.py

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from users.models import UserTypes
from .roles import ROLES


def is_self(request, view, obj=None):
    """
    Проверяет, что created_by_id у объекта совпадает с request.user.id.
    Для object-level пермишнов.
    """
    if obj is None:
        obj = view.get_object()
    return getattr(obj, 'created_by_id', None) == request.user.id


class RolesPermission(permissions.BasePermission):
    """
    Доступ по роли из UserTypes + кастомные чекеры из ROLES.
    """

    def has_permission(self, request, view):
        perms_map = view.get_view_permissions().get(view.action, {})
        return self._check_role(request, view, perms_map, None)

    def has_object_permission(self, request, view, obj):
        perms_map = view.get_view_permissions().get(view.action, {})
        return self._check_role(request, view, perms_map, obj)

    def _check_role(self, request, view, perms_map, obj):
        # если неавторизованный — сводим всё к одной роли 'ANON'
        if request.user.is_anonymous:
            user_role = 'ANON'
        else:
            user_role = UserTypes(request.user.user_type).name.upper()

        # нормализуем ключи из view_permissions
        normalized = {
            raw_role.upper(): checker
            for raw_role, checker in perms_map.items()
        }
        checker = normalized.get(user_role)
        if not checker:
            return False

        # если прописано True — используем функцию из ROLES
        if checker is True:
            role_fn = ROLES.get(user_role) or ROLES.get(user_role.lower())
            if not role_fn:
                return False
            return role_fn(request, view, obj=obj) if obj is not None else role_fn(request, view)

        # если кастомная функция — вызываем её
        if callable(checker):
            return checker(request, view, obj=obj) if obj is not None else checker(request, view)

        return False
