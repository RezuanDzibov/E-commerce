from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """ If requested user isn't in the stuff group, then allows only read"""
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )
