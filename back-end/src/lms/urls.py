from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.students import StudentViewSet, ActivateStudentReadonlyViewSet
from lms.views.teachers import TeacherViewSet
from lms.views.absences import AbsenceViewSet, AbsenceJournalView
from lms.views.absence_time import AbsenceTimeView
from lms.views.punishments import PunishmentViewSet
from lms.views.encouragements import EncouragementViewSet
from lms.views.achievements import AchievementViewSet
from lms.views.reference_book import (
    ReferenceBookView,
    MilfacultyViewSet,
    MilspecialtyViewSet,
    MilgroupViewSet,
    ProgramViewSet,
    RankViewSet,
    TeacherPostViewSet,
    RoomViewSet,
    AchievementTypeViewSet,
)
from lms.views.subjects import LessonSubjectViewSet
from lms.views.lessons import LessonViewSet, LessonJournalView
from lms.views.marks import MarkViewSet, MarkJournalView

routers = DefaultRouter()
routers.register('students', StudentViewSet)
routers.register('teachers', TeacherViewSet)
routers.register('absences', AbsenceViewSet)
routers.register('punishments', PunishmentViewSet)
routers.register('encouragements', EncouragementViewSet)
routers.register('subjects', LessonSubjectViewSet)
routers.register('achievements', AchievementViewSet)
routers.register('lessons', LessonViewSet)
routers.register('marks', MarkViewSet)
routers.register('milfaculties', MilfacultyViewSet)
routers.register('milspecialties', MilspecialtyViewSet)
routers.register('milgroups', MilgroupViewSet)
routers.register('programs', ProgramViewSet)
routers.register('ranks', RankViewSet)
routers.register('teacher-posts', TeacherPostViewSet)
routers.register('rooms', RoomViewSet)
routers.register('achievement-types', AchievementTypeViewSet)
routers.register('activate-students', ActivateStudentReadonlyViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
    path('reference-book/', ReferenceBookView.as_view()),
    path('lesson-journal/', LessonJournalView.as_view()),
    path('mark-journal/', MarkJournalView.as_view()),
    path('absence-time/', AbsenceTimeView.as_view()),
]
