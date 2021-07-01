from django.db.models import QuerySet

from rest_framework import status
from rest_framework.response import Response

from lms.functions import get_user_from_request

from auth.models import Permission, User


class QuerysetScopingMixin:

    scoped_permission_class = None

    # Scoping for getting the queryset
    # (applies to GET (all or by id),
    # PUT, PATCH AND DELETE)

    def handle_scope_all(self) -> QuerySet:
        return self.queryset

    # pylint: disable=unused-argument
    def handle_scope_milfaculty(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_milgroup(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_self(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=too-many-return-statements
    def get_queryset(self) -> QuerySet:
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

    # Scoping for creation
    # (applies to POST)

    # pylint: disable=unused-argument
    def handle_scope_milfaculty_on_create(self, data: dict, user_type: str,
                                          user: User) -> bool:
        return False

    # pylint: disable=unused-argument
    def handle_scope_milgroup_on_create(self, data: dict, user_type: str,
                                        user: User) -> bool:
        return False

    # pylint: disable=unused-argument
    def handle_scope_self_on_create(self, data: dict, user_type: str,
                                    user: User) -> bool:
        return False

    # pylint: disable=too-many-return-statements
    def is_creation_allowed_by_scope(self, data: dict) -> bool:
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scopes.ALL:
            return True

        # check if user is a teacher ot a student
        user_type, user = get_user_from_request(self.request)
        if user is None:
            # return False if user is not a student or a teacher
            return False

        if scope == Permission.Scopes.MILFACULTY:
            return self.handle_scope_milfaculty_on_create(data, user_type, user)

        if scope == Permission.Scopes.MILGROUP:
            return self.handle_scope_milgroup_on_create(data, user_type, user)

        if scope == Permission.Scopes.SELF:
            return self.handle_scope_self_on_create(data, user_type, user)

        return False

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN)
