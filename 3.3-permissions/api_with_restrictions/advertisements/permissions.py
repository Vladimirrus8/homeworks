from rest_framework import permissions


class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Разрешение на редактирование/удаление:
    - только автору объявления
    - или администратору
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user or request.user.is_staff


class IsNotCreator(permissions.BasePermission):
    """Запрещаем автору добавлять своё объявление в избранное"""

    def has_object_permission(self, request, view, obj):
        return obj.creator != request.user