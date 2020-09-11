from django.urls import path
from lms.views.student import StudentView
from lms.views.teacher import TeacherView
from lms.views.absence import AbsenceView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
    path('absence/', AbsenceView.as_view()),
]
