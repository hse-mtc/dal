from django.contrib import admin

from lms.models.encouragements import Encouragement
from lms.models.punishments import Punishment
from lms.models.teachers import Teacher
from lms.models.marks import Mark
from lms.models.uniforms import Uniform
from lms.models.absences import (
    Absence,
    AbsenceTime,
)
from lms.models.common import (
    Milgroup,
    Milfaculty,
)
from lms.models.achievements import (
    AchievementType,
    Achievement,
)
from lms.models.students import (
    Student,
    Note,
    Skill,
)
from lms.models.lessons import (
    Room,
    Lesson,
)

# Common
admin.site.register(Milfaculty)
admin.site.register(Milgroup)

# Students
admin.site.register(Note)
admin.site.register(Skill)
admin.site.register(Student)

# Teachers
admin.site.register(Teacher)

# Marks
admin.site.register(Mark)

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

# Uniforms
admin.site.register(Uniform)
