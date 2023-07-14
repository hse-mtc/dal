from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.achievements import AchievementViewSet
from lms.views.import_schedule import ParseScheduleView, ImportParsedView
from lms.views.personnel import SearchPersonnelUsersViewSet
from lms.views.subjects import LessonSubjectViewSet
from lms.views.uniforms import UniformViewSet
from lms.views.absences import (
    AbsenceViewSet,
    AbsenceJournalView,
    AbsenceTimeView,
    AbsenceAttachmentViewSet,
    AbsenceExcuseChoicesList,
    AbsenceStatusChoicesList,
)
from lms.views.encouragements import (
    EncouragementViewSet,
    EncouragementTypeChoicesList,
)
from lms.views.lessons import (
    LessonViewSet,
    LessonJournalView,
    LessonTypeChoicesList,
)
from lms.views.marks import (
    MarkViewSet,
    MarkJournalView,
)
from lms.views.punishments import (
    PunishmentViewSet,
    PunishmentTypeChoicesList,
)
from lms.views.students import (
    StudentViewSet,
    ActivateStudentViewSet,
    NoteViewSet,
    StudentStatusChoicesList,
    StudentPostChoicesList,
    ApproveStudentViewSet,
)
from lms.views.teachers import (
    TeacherViewSet,
    ApproveTeacherViewSet,
    TeacherRankChoicesList,
    TeacherPostChoicesList,
)
from lms.views.dashboard import (
    StudentBasicInfoViewSet,
    StudentExtraInfoViewSet,
    StudentPerformanceView,
    StudentSkillsView,
)
from lms.views.birthdays import (
    StudentBirthdayAlertView,
    TeacherBirthdayAlertView,
)
from lms.views.reference_book import (
    ReferenceBookView,
    MilfacultyViewSet,
    MilspecialtyViewSet,
    MilgroupViewSet,
    ProgramViewSet,
    RoomViewSet,
    AchievementTypeViewSet,
    SkillViewSet,
    MilgroupLeadersView,
)

routers = DefaultRouter()

routers.register("students/notes", NoteViewSet)
routers.register("students/approvals", ActivateStudentViewSet)
routers.register("students/basic", StudentBasicInfoViewSet)
routers.register("students/extra", StudentExtraInfoViewSet)
routers.register("students/skills", StudentSkillsView)
routers.register("students/approval-for-existing-students", ApproveStudentViewSet)
routers.register("students", StudentViewSet)

routers.register("teachers/approvals", ApproveTeacherViewSet)
routers.register("teachers", TeacherViewSet)

routers.register("absences", AbsenceViewSet)
routers.register("absence-attachments", AbsenceAttachmentViewSet)
routers.register("achievement-types", AchievementTypeViewSet)
routers.register("achievements", AchievementViewSet)
routers.register("encouragements", EncouragementViewSet)
routers.register("lessons", LessonViewSet)
routers.register("marks", MarkViewSet)
routers.register("milfaculties", MilfacultyViewSet)
routers.register("milgroups", MilgroupViewSet)
routers.register("milspecialties", MilspecialtyViewSet)
routers.register("personnel-users", SearchPersonnelUsersViewSet)
routers.register("programs", ProgramViewSet)
routers.register("punishments", PunishmentViewSet)
routers.register("rooms", RoomViewSet)
routers.register("skills", SkillViewSet)
routers.register("subjects", LessonSubjectViewSet)
routers.register("uniforms", UniformViewSet)


choices = [
    path("absence-excuses/", AbsenceExcuseChoicesList.as_view()),
    path("absence-statuses/", AbsenceStatusChoicesList.as_view()),
    path("encouragement-types/", EncouragementTypeChoicesList.as_view()),
    path("lesson-types/", LessonTypeChoicesList.as_view()),
    path("punishment-types/", PunishmentTypeChoicesList.as_view()),
    path("student-posts/", StudentPostChoicesList.as_view()),
    path("student-statuses/", StudentStatusChoicesList.as_view()),
    path("teacher-posts/", TeacherPostChoicesList.as_view()),
    path("teacher-ranks/", TeacherRankChoicesList.as_view()),
]

urlpatterns = [
    # Router.
    path("", include(routers.urls)),
    # Manual.
    path("absence-journal/", AbsenceJournalView.as_view()),
    path("reference-book/", ReferenceBookView.as_view()),
    path("lesson-journal/", LessonJournalView.as_view()),
    path("mark-journal/", MarkJournalView.as_view()),
    path("absence-time/", AbsenceTimeView.as_view()),
    path("students/<int:pk>/performance/", StudentPerformanceView.as_view()),
    path("milgroup-leaders/", MilgroupLeadersView.as_view()),
    path("birthdays/students", StudentBirthdayAlertView.as_view()),
    path("birthdays/teachers", TeacherBirthdayAlertView.as_view()),
    path("import-schedule/parse-schedule/", ParseScheduleView.as_view()),
    path("import-schedule/save-parsed/", ImportParsedView.as_view()),
    # Choices lists.
    path("choices/", include(choices)),
]
