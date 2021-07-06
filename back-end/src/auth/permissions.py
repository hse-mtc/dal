from rest_framework import permissions

from auth.models import Permission


class BasePermission(permissions.BasePermission):
    permission_class = ""
    view_name_rus = ""
    methods = ["get", "put", "post", "patch", "delete"]
    scopes = [
        Permission.Scope.ALL,
    ]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # check for method permission
        return request.user.has_general_perm(self.permission_class,
                                             request.method)


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
