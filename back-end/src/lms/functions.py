from datetime import timedelta, datetime

from rest_framework.request import Request

from lms.models.students import Student
from lms.models.teachers import Teacher

from auth.models import Permission
from auth.permissions import BasePermission


def get_user_from_request(request):
    """
    Get user from request.
    Returns empty string and None if user is not
    a teacher or a student.

    :param request: REST/HTTP request
    :return: user_type (str), user (User object)
    """
    # check if user is a teacher or a student
    candidates = [Teacher, Student]

    for candidate in candidates:
        if (user := candidate.objects.filter(user=request.user)).exists():
            return candidate.__name__.lower(), user.first()

    return '', None


# pylint: disable=too-many-return-statements
def milgroup_allowed_by_scope(milgroup: dict, request: Request,
                              permission_class: BasePermission) -> bool:
    """
    Check if specified milgroup is compatible with permission scope.
    Used in Journal views.

    :param milgroup: serialized milgroup
    (query param in journal get request)
    :param request: request
    :param permission_class: Scoped permission class

    :return: bool: allowed (True) or not allowed (False)
    """
    if request.user.is_superuser:
        return True

    scope = request.user.get_perm_scope(permission_class.permission_class,
                                        request.method)

    if scope == Permission.Scope.ALL:
        return True

    # check if user is a teacher ot a student
    user_type, user = get_user_from_request(request)
    if user is None:
        return False

    if scope == Permission.Scope.MILFACULTY:
        if user_type == 'student':
            milfaculty = user.milgroup.milfaculty
        elif user_type == 'teacher':
            milfaculty = user.milfaculty
        else:
            return False
        return milgroup['milfaculty'] == milfaculty.milfaculty

    if scope == Permission.Scope.MILGROUP:
        if user_type in ('student', 'teacher'):
            return milgroup['milgroup'] == user.milgroup.milgroup
        return False

    return False


def get_date_range(date_from: datetime, date_to: datetime,
                   weekday: int) -> list[str]:
    """
    Calculate dates with the same weekday from the date range provided

    :param date_from: starting date range
    :param date_to: ending date range
    :param weekday: weekday number [0;6]  (0-Monday)
    :return: array of dates
    """
    start_date = date_from + timedelta((weekday - date_from.weekday() + 7) % 7)

    dates = []
    cur_date = start_date

    while cur_date <= date_to:
        dates.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(7)

    return dates
