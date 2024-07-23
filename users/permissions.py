from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
