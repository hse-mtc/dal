from django.urls import path

from lms.views.student import StudentViewSet
from lms.views.teacher import TeacherViewSet
from lms.views.absence import AbsenceViewSet, AbsenceJournalView

list_view_map = {
    'get': 'list',
    'put': 'create',
}
detail_view_map = {
    'get': 'retrieve',
    'post': 'update',
    'delete': 'destroy',
}

urlpatterns = [
    path('student/', StudentViewSet.as_view(list_view_map)),
    path('student/<int:pk>', StudentViewSet.as_view(detail_view_map)),
    path('teacher/', TeacherViewSet.as_view(list_view_map)),
    path('teacher/<int:pk>', TeacherViewSet.as_view(detail_view_map)),
    path('absence/', AbsenceViewSet.as_view(list_view_map)),
    path('absence/<int:pk>', AbsenceViewSet.as_view(detail_view_map)),
    path('absence-journal/', AbsenceJournalView.as_view()),
]
