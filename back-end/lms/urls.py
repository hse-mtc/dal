from django.urls import path
from lms.views.student import StudentView
from lms.views.teacher import TeacherView
from lms.views.absence import AbsenceView, AbsenceJournalView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
    path('absence/', AbsenceView.as_view()),
    path('absence_journal/', AbsenceJournalView.as_view()),
]
