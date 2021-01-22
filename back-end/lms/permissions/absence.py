from rest_framework.permissions import BasePermission


class AbsencePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'GET':
            return request.user.has_perm(
                'auth.absence_get') or request.user.has_perm(
                    'auth.absence_full')
        return request.user.has_perm('auth.absence_full')
