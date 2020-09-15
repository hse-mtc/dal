from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.student import StudentView
from lms.views.teacher import TeacherView
from lms.views.absence import AbsenceView

from lms.views.student2 import StudentViewSet


router = DefaultRouter()
router.register('student2', StudentViewSet)

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
    path('absence/', AbsenceView.as_view()),
]

urlpatterns += router.urls
