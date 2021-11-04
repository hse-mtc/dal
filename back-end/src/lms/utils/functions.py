import typing as tp

from rest_framework.request import Request

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.common import Milgroup
from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.types.personnel import Personnel


def get_personnel_from_request_user(user) -> tp.Optional[Personnel]:
    """Get Personnel object from the user of the incoming request.

    Args:
        user: REST/HTTP request user.

    Returns:
        personnel: Personnel object.
    """

    candidates = ["student", "teacher"]

    for candidate in candidates:
        if hasattr(user, candidate):
            return getattr(user, candidate)

    return None


# pylint: disable=too-many-return-statements
def milgroup_allowed_by_scope(
    milgroup: Milgroup,
    request: Request,
    permission_class: tp.Type[BasePermission],
) -> bool:
    """
    Check if specified milgroup is compatible with permission scope.
    Used in Journal views.

    :param milgroup: Milgroup object
    :param request: DRF request
    :param permission_class: Scoped permission class

    :return: bool: allowed (True) or not allowed (False)
    """

    if request.user.is_superuser:
        return True

    scope = request.user.get_perm_scope(
        permission_class.permission_class,
        request.method,
    )

    if scope == Permission.Scope.ALL:
        return True

    user = get_personnel_from_request_user(request.user)
    if user is None:
        return False

    user: Personnel

    if scope == Permission.Scope.MILFACULTY:
        match user:
            case Student() | Teacher():
                milfaculty = user.milfaculty
            case _:
                assert False, "Unhandled Personnel type"
        return milgroup.milfaculty == milfaculty

    if scope in [Permission.Scope.MILGROUP, Permission.Scope.SELF]:
        match user:
            case Student():
                return milgroup == user.milgroup
            case Teacher():
                return milgroup in user.milgroups
            case _:
                assert False, "Unhandled Personnel type"

    return False
