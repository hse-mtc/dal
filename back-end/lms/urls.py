from django.urls import path, include

from lms.views.student import StudentView
from lms.views.teacher import TeacherView
from lms.views.absence import AbsenceView

from lms.views.student2 import StudentViewSet


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
    path('student/', StudentView.as_view()),
    path('teacher/', TeacherView.as_view()),
    path('absence/', AbsenceView.as_view()),
    path('student2/', StudentViewSet.as_view(list_view_map)),
    path('student2/<int:pk>/', StudentViewSet.as_view(detail_view_map)),
]
