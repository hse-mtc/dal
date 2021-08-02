from datetime import timedelta, datetime

from rest_framework.request import Request

from lms.models.common import Milgroup

from auth.models import Permission
from auth.permissions import BasePermission


def get_user_from_request(user):
    """
    Get Teacher/Student user from request.
    Returns empty string and None if user is not
    a teacher or a student.

    :param user: user from REST/HTTP request
    :return: user_type (str), user (User object)
    """
    # check if user is a teacher or a student

    candidates = ["teacher", "student"]

    for candidate in candidates:
        if hasattr(user, candidate):
            return candidate, getattr(user, candidate)

    return "", None


# pylint: disable=too-many-return-statements
def milgroup_allowed_by_scope(
    milgroup: Milgroup,
    request: Request,
    permission_class: BasePermission,
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

    scope = request.user.get_perm_scope(permission_class.permission_class,
                                        request.method)

    if scope == Permission.Scope.ALL:
        return True

    # check if user is a teacher ot a student
    user_type, user = get_user_from_request(request.user)
    if user is None:
        return False

    if scope == Permission.Scope.MILFACULTY:
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return False
        return milgroup.milfaculty == milfaculty

    if scope in [Permission.Scope.MILGROUP, Permission.Scope.SELF]:
        if user_type == "student":
            return milgroup == user.milgroup
        if user_type == "teacher":
            return milgroup in user.milgroups
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
        dates.append(cur_date.strftime("%Y-%m-%d"))
        cur_date += timedelta(7)

    return dates


def get_current_semester_range() -> tuple[datetime, datetime]:
    first_semester_months = list(range(9, 13))
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    if current_month in first_semester_months:
        return datetime(current_year, 9, 1), datetime(current_year, 12, 31)
    return datetime(current_year, 1, 1), datetime(current_year, 8, 31)


def get_today_date_rus() -> str:
    today = datetime.today()
    months = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    return f"\"{today.day}\"  {months[today.month-1]}  {today.year} г."