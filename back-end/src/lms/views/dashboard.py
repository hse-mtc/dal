from statistics import mean

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.views import extend_schema

from lms.models.marks import Mark
from lms.models.absences import Absence


@extend_schema(tags=["students"])
class StudentPerformanceView(APIView):

    # pylint:disable=("invalid-name")
    def get(self, request: Request, pk: int) -> Response:
        marks = Mark.objects.filter(student=pk).select_related(
            "lesson", "lesson__subject")
        absences_dates = Absence.objects.filter(student=pk).values_list("date")
        absences_dates = [date[0] for date in absences_dates]
        student_subject_marks = {}
        subject_dates = {}
        response = []
        # find all marks for subject
        for mark in marks:
            student_subject_marks.setdefault(mark.lesson.subject.title,
                                             []).append(*mark.mark)
            subject_dates.setdefault(mark.lesson.subject.title,
                                     []).append(mark.lesson.date)

        for subject in student_subject_marks:
            student_subject_marks[subject] = mean(
                student_subject_marks[subject])

        for subject in subject_dates:
            subject_dates[subject] = len(
                set(absences_dates) & set(subject_dates[subject]))

        for subject, avg_mark in student_subject_marks.items():
            subject_info = {
                "discipline": subject,
                "average_mark": avg_mark,
                "absences": subject_dates[subject]
            }
            response.append(subject_info)
        return Response(response)
