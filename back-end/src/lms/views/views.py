from django.db.models import QuerySet

from lms.functions import get_user_from_request

from auth.models import Permission


class BasicQuerysetScoping:

    scoped_permission_class = None
    queryset = QuerySet()

    def handle_scope_all(self):
        return self.queryset

    # pylint: disable=unused-argument
    def handle_scope_milfaculty(self, user_type, user):
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_milgroup(self, user_type, user):
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_self(self, user_type, user):
        return self.queryset.none()

    # pylint: disable=too-many-return-statements
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scopes.ALL:
            return self.handle_scope_all()

        # check if user is a teacher ot a student
        user_type, user = get_user_from_request(self.request)
        if user is None:
            # return nothing if user is not a student or a teacher
            return self.queryset.none()

        if scope == Permission.Scopes.MILFACULTY:
            return self.handle_scope_milfaculty(user_type, user)

        if scope == Permission.Scopes.MILGROUP:
            return self.handle_scope_milgroup(user_type, user)

        if scope == Permission.Scopes.SELF:
            return self.handle_scope_self(user_type, user)

        return self.queryset.none()
