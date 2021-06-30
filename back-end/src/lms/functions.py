from datetime import timedelta, datetime
from lms.models.students import Student
from lms.models.teachers import Teacher


def get_user_from_request(request):
    """
    Get user from request.
    Returns empty string and None if user is not
    a teacher or a student.

    :param request: REST/HTTP request
    :return: user_type (str), user (User object)
    """
    # check if user is a teacher or a student
    user = Teacher.objects.filter(user=request.user)
    user_type = 'teacher'
    if user.count() == 0:
        # check if user is a student
        user = Student.objects.filter(user=request.user)
        user_type = 'student'
        if user.count() == 0:
            return '', None
    return user_type, user.first()


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
