from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_field = getattr(view, 'user_field', 'user')
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, user_field) == request.user
