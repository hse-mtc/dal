from django.urls import path
from mil_lms_backend.views.student import StudentView

urlpatterns = [
    path('student/', StudentView.as_view()),
]
