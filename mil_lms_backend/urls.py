from django.urls import path
from mil_lms_backend.views.student import StudentView
from mil_lms_backend.views.teachers import TeacherView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
]
