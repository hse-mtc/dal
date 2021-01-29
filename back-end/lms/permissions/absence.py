from auth.permissions import BasicPermission


class AbsencePermission(BasicPermission):
    permission_get = 'auth.absence_get'
    permission_full = 'auth.absence_full'
