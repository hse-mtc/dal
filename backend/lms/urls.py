from django.urls import path
from lms.views.student import StudentView
from lms.views.absence import AbsenceView

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('absence/', AbsenceView.as_view()),
]
