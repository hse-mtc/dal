from django.contrib import admin

from lms.models.encouragements import Encouragement
from lms.models.punishments import Punishment
from lms.models.applicants import ApplicationProcess
from lms.models.absences import (
    Absence,
    AbsenceTime,
)
from lms.models.universities import (
    Program,
    UniversityInfo,
)
from lms.models.common import (
    Milgroup,
    Milfaculty,
    Milspecialty,
)
from lms.models.teachers import (
    Rank,
    Teacher,
)
from lms.models.achievements import (
    AchievementType,
    Achievement,
)
from lms.models.students import (
    Student,
    Note,
    RecruitmentOffice,
)
from lms.models.lessons import (
    Room,
    Lesson,
)

# Common
admin.site.register(Milfaculty)
admin.site.register(Milspecialty)
admin.site.register(Milgroup)

# Students
admin.site.register(Student)
admin.site.register(RecruitmentOffice)
admin.site.register(Note)

# Applicants
admin.site.register(ApplicationProcess)

# Universities
admin.site.register(Program)
admin.site.register(UniversityInfo)

# Teachers
admin.site.register(Rank)
admin.site.register(Teacher)

# Lessons
admin.site.register(Room)
admin.site.register(Lesson)

# Absences
admin.site.register(Absence)
admin.site.register(AbsenceTime)

# Encouragements
admin.site.register(Encouragement)

# Punishments
admin.site.register(Punishment)

# Achievements
admin.site.register(AchievementType)
admin.site.register(Achievement)
