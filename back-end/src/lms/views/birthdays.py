from datetime import date

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.views import extend_schema

from lms.models.students import Student
from lms.models.teachers import Teacher


class BirthdayAlertView(APIView):
    model = None

    def get(self, request: Request) -> Response:
        persons = self.model.get_nearest_birthdays()
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


@extend_schema(tags=["birthday"])
class TeacherBirthdayAlertView(BirthdayAlertView):
    model = Teacher
