from django.core.management.base import BaseCommand

from auth.models import Permission
from auth.permissions import BasePermission


class Command(BaseCommand):
    help = "Save all registered permissions in the database."

    def register_view_permissions(self, perm_class: BasePermission):
        methods_str = perm_class.methods_str

        scopes_str = {
            Permission.Scope.SELF: ", связанных с пользователем",
            Permission.Scope.MILGROUP: " о взводе, связанным с пользователем",
            Permission.Scope.MILFACULTY: " о цикле, связанным с пользователем",
            Permission.Scope.ALL: " (всех данных)",
        }

        permissions = []
        for method in perm_class.methods:
            for scope in perm_class.scopes:
                permissions.append({
                    "viewset":
                        perm_class.permission_class,
                    "method":
                        method,
                    "scope":
                        scope,
                    "name":
                        "".join([
                            perm_class.view_name_rus, methods_str[method],
                            scopes_str[scope]
                        ]),
                })

        for val in permissions:
            Permission.objects.get_or_create(**val)

    def handle(self, *args, **options):
        # Info about permissions that must be saved in db could
        # be received from BasePermission subclasses
        for perm_class in BasePermission.__subclasses__():
            self.register_view_permissions(perm_class)
