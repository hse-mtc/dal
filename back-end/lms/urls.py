from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.student import StudentViewSet
from lms.views.teacher import TeacherViewSet
from lms.views.absence import AbsenceViewSet, AbsenceJournalView
from lms.views.punishment import PunishmentViewSet
from lms.views.encouragement import EncouragementViewSet
from lms.views.achievement import AchievementViewSet
from lms.views.reference_book import ReferenceBookView
from lms.views.subject import LessonSubjectViewSet
from lms.views.lesson import LessonViewSet, LessonJournalView
from lms.views.mark import MarkViewSet


routers = DefaultRouter()
routers.register('student', StudentViewSet)
routers.register('teacher', TeacherViewSet)
routers.register('absence', AbsenceViewSet)
routers.register('punishment', PunishmentViewSet)
routers.register('encouragement', EncouragementViewSet)
routers.register('subject', LessonSubjectViewSet)
routers.register('achievement', AchievementViewSet)
routers.register('lesson', LessonViewSet)
routers.register('mark', MarkViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
    path('reference-book/', ReferenceBookView.as_view()),
    path('lesson-journal/', LessonJournalView.as_view()),
]
