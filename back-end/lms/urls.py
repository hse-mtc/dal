from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.viewsets import StudentViewSet, TeacherViewSet
from lms.views.absence import AbsenceViewSet, AbsenceJournalView


routers = DefaultRouter()
routers.register('student', StudentViewSet)
routers.register('teacher', TeacherViewSet)
routers.register('absence', AbsenceViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
]
