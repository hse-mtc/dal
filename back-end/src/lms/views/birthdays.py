from datetime import date

from django.db.models import QuerySet

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.views import extend_schema

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.functions import get_user_from_request


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

    def get_birthdays(self) -> QuerySet:
        return self.model.get_nearest_birthdays()

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
                "full_name": person.full_name,
                "how_old_will_be": how_old,
            }
            response.append(temp)
        return Response(response)


@extend_schema(tags=["birthday"])
class StudentBirthdayAlertView(BirthdayAlertView):
    model = Student

    permission_classes = [StudentBirthdayAlertPermission]
    scoped_permission_class = StudentBirthdayAlertPermission

    def get_milfaculty_scope_filter(self, user_type, user) -> dict:
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return {"milgroup__archived": False}
        return {
            "milgroup__archived": False,
            "milgroup__milfaculty": milfaculty,
        }

    def get_birthdays(self) -> QuerySet:
        params = {"milgroup__archived": False}

        if self.request.user.is_superuser:
            return self.model.get_nearest_birthdays(params)

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return self.model.get_nearest_birthdays(params)

        # check if user is a teacher ot a student
        user_type, user = get_user_from_request(self.request.user)
        if user is None:
            # return nothing if user is not a student or a teacher
            return QuerySet()

        if scope == Permission.Scope.MILFACULTY:
            params = self.get_milfaculty_scope_filter(user_type, user)
            return self.model.get_nearest_birthdays(params)
        
        return QuerySet()


@extend_schema(tags=["birthday"])
class TeacherBirthdayAlertView(BirthdayAlertView):
    model = Teacher

    permission_classes = [TeacherBirthdayAlertPermission]
