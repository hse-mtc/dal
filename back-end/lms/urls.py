from django.urls import path, include

from lms.views.absence import AbsenceView

from lms.views.student import StudentViewSet
from lms.views.teacher import TeacherViewSet


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
    path('absence/', AbsenceView.as_view()),
]
