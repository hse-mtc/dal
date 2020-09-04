from django.urls import path
from mil_lms_backend.views.student import StudentView
<<<<<<< HEAD
from mil_lms_backend.views.teacher import TeacherView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
=======
from mil_lms_backend.views.absence import AbsenceView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('absence/', AbsenceView.as_view()),
>>>>>>> master
]
