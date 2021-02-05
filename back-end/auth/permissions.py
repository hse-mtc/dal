import copy
from rest_framework import permissions


class DjangoModelPermissionsWithGet(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class BasicPermission(permissions.BasePermission):
    permission_class = ''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # check for method permission
        return request.user.has_perm(self.permission_class + '_' +
                                     request.method.lower())
