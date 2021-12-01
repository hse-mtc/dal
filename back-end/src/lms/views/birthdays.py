import typing as tp

from datetime import (
    date,
    timedelta,
)

from django.db import models

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.views import extend_schema

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.utils.functions import get_personnel_from_request_user


class StudentBirthdayAlertPermission(BasePermission):
    permission_class = "student-birthday-alert"
    view_name_rus = "Оповещения о днях рождениях студентов"
    methods = ["get"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
    ]


class TeacherBirthdayAlertPermission(BasePermission):
    permission_class = "teacher-birthday-alert"
    view_name_rus = "Оповещения о днях рождениях преподавателей"
    methods = ["get"]


class BirthdayAlertView(APIView):
    model = None

    def get_birthdays(self) -> models.QuerySet:
        return get_nearest_birthdays(self.model)

    def get(self, request: Request) -> Response:
        persons = self.get_birthdays()
        today = date.today()

        response = []

        for person in persons:
            born = person.birth_info.date
            will_have_bd = date(
                day=born.day,
                month=born.month,
                year=today.year,
            )
            if will_have_bd < today:
                will_have_bd = will_have_bd.replace(year=today.year + 1)

            how_old = will_have_bd.year - born.year

            temp = {
                "id": person.id,
                "birthday": born,
                "fullname": person.fullname,
                "how_old_will_be": how_old,
            }
            response.append(temp)
        return Response(response)


@extend_schema(tags=["birthday"])
class StudentBirthdayAlertView(BirthdayAlertView):
    model = Student

    permission_classes = [StudentBirthdayAlertPermission]
    scoped_permission_class = StudentBirthdayAlertPermission

    def get_milfaculty_scope_filter(self, personnel) -> dict:
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return {
            "milgroup__archived": False,
            "milgroup__milfaculty": milfaculty,
        }

    def get_birthdays(self) -> models.QuerySet:
        params = {"milgroup__archived": False}

        if self.request.user.is_superuser:
            return get_nearest_birthdays(self.model, params)

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return get_nearest_birthdays(self.model, params)

        user = get_personnel_from_request_user(self.request.user)

        # return nothing if user is not a student or a teacher
        if user is None:
            return self.model.objects.none()

        if scope == Permission.Scope.MILFACULTY:
            params = self.get_milfaculty_scope_filter(user)
            return get_nearest_birthdays(self.model, params)

        return self.model.objects.none()


@extend_schema(tags=["birthday"])
class TeacherBirthdayAlertView(BirthdayAlertView):
    model = Teacher

    permission_classes = [TeacherBirthdayAlertPermission]


def get_nearest_birthdays(
    model: tp.Type[models.Model],
    filter_kwargs: tp.Optional[dict] = None
) -> models.QuerySet:
    """Return personnel with birthdays that are in one week to today's date.

    Args:
        model: Django model to filter.
        filter_kwargs: additional filters.

    Returns:
        Filtered queryset.
    """

    today = date.today()
    start, end = today, today + timedelta(days=7)
    return model.objects.select_related("birth_info").filter(
        birth_info__date__day__gte=start.day,
        birth_info__date__day__lte=end.day,
        birth_info__date__month__gte=start.month,
        birth_info__date__month__lte=end.month,
        **({} if filter_kwargs is None else filter_kwargs),
    ).order_by("birth_info__date")
