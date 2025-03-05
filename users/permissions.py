from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False
