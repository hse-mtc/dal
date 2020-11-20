from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.student import StudentViewSet
from lms.views.teacher import TeacherViewSet
from lms.views.absence import AbsenceViewSet, AbsenceJournalView
from lms.views.punishment import PunishmentViewSet
from lms.views.encouragement import EncouragementViewSet
from lms.views.reference_book import ReferenceBookView

routers = DefaultRouter()
routers.register('student', StudentViewSet)
routers.register('teacher', TeacherViewSet)
routers.register('absence', AbsenceViewSet)
routers.register('punishment', PunishmentViewSet)
routers.register('encouragement', EncouragementViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
    path('reference-book/', ReferenceBookView.as_view())
]
