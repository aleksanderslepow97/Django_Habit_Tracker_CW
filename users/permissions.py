from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Проверяет, является ли пользователь создателем."""

    message = "Вы не являетесь создателем этой привычки!"

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.user == request.user

    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_authenticated
