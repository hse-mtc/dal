from rest_framework import permissions

from auth.models import Permission


def register_view_permissions(view_name, view_name_rus, 
                                methods=["get", "post", "patch", "delete"], 
                                scopes=["self", "milgroup", "milfaculty", "all"]):
    methods_str = {
        "get": ": получение данных",
        "post": ": добавление данных",
        "patch": ": редактирование данных",
        "delete": ": удаление данных",
    }

    scopes_str = {
        "self": (int(Permission.Scopes.SELF), ", связанных с пользователем"),
        "milgroup": (int(Permission.Scopes.MILGROUP),
                     " о взводе, связанным с пользователем"),
        "milfaculty": (int(Permission.Scopes.MILFACULTY),
                       " о цикле, связанным с пользователем"),
        "all": (int(Permission.Scopes.ALL), " (всех данных)"),
    }

    permissions = []
    for method in methods:
        for scope in scopes:
            permissions.append({
                "viewset":
                    view_name,
                "method":
                    method,
                "scope":
                    scopes_str[scope][0],
                "name":
                    "".join([
                        view_name_rus, methods_str[method], scopes_str[scope][1]
                    ]),
            })

    for val in permissions:
        Permission.objects.get_or_create(
            viewset=val["viewset"],
            method=val["method"],
            scope=val["scope"],
            name=val["name"],
        )


class BasePermission(permissions.BasePermission):
    permission_class = ""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # check for method permission
        return request.user.has_general_perm(self.permission_class,
                                             request.method)


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
