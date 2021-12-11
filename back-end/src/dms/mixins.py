from rest_framework import status
from rest_framework.response import Response

from auth.models import Permission


class QuerySetScopingByUserMixin:
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF:
            return self.queryset.filter(user=self.request.user)

        return self.queryset.none()

    def is_creation_allowed_by_scope(self, data):
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return True

        if scope == Permission.Scope.SELF:
            return self.request.user.id == data["user"]
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
