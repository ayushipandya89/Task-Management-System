from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions


class IsOwnerOrAdminForTaskList(permissions.BasePermission):
    """
    Custom permission to allow only the owner of the task list or admin users (is_admin=True or is_superuser=True) to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_admin:
            return True
        return obj.owner == request.user


class IsAuthorizedForTaskList(DjangoModelPermissions):
    """
    Custom permission to check permissions for task lists table.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_tasklist'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_tasklist'],
        'PUT': ['%(app_label)s.change_tasklist'],
        'PATCH': [],
        'DELETE': ['%(app_label)s.delete_tasklist']
    }


class IsAuthorizedForTask(DjangoModelPermissions):
    """
    Custom permission to check permissions for task table.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_task'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_task'],
        'PUT': ['%(app_label)s.change_task'],
        'PATCH': [],
        'DELETE': ['%(app_label)s.delete_task']
    }


class IsOwnerOrAdminForTask(permissions.BasePermission):
    """
    Custom permission to allow only the owner of the task list or admin users (is_admin=True or is_superuser=True) to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.assigned_to == request.user or obj.created_by == request.user or request.user.is_superuser or request.user.is_admin
        return request.user.is_superuser or request.user.is_admin or obj.created_by == request.user


