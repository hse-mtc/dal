from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.student import StudentViewSet
from lms.views.teacher import TeacherViewSet
from lms.views.absence import AbsenceViewSet, AbsenceJournalView
from lms.views.punishment import PunishmentViewSet
from lms.views.encouragement import EncouragementViewSet
from lms.views.achievement import AchievementViewSet
from lms.views.reference_book import ReferenceBookView
from lms.views.subject import SubjectViewSet
from lms.views.lesson import LessonViewSet

routers = DefaultRouter()
routers.register('student', StudentViewSet)
routers.register('teacher', TeacherViewSet)
routers.register('absence', AbsenceViewSet)
routers.register('punishment', PunishmentViewSet)
routers.register('encouragement', EncouragementViewSet)
routers.register('subject', SubjectViewSet)
routers.register('achievement', AchievementViewSet)
routers.register('lesson', LessonViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
    path('reference-book/', ReferenceBookView.as_view())
]
