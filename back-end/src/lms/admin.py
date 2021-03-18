from django.contrib import admin

from lms.models.common import Milgroup, Milfaculty, Milspecialty
from lms.models.students import Student
from lms.models.teachers import Rank, TeacherPost, Teacher
from lms.models.absences import Absence
from lms.models.encouragements import Encouragement
from lms.models.punishments import Punishment
from lms.models.achievements import AchievementType, Achievement
from lms.models.lessons import Room, Lesson

# Registering reference models
admin.site.register(Milfaculty)
admin.site.register(Milspecialty)
admin.site.register(Rank)
admin.site.register(TeacherPost)
admin.site.register(AchievementType)
admin.site.register(Room)

# Registering other models
admin.site.register(Milgroup)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Absence)
admin.site.register(Encouragement)
admin.site.register(Punishment)
admin.site.register(Achievement)
admin.site.register(Lesson)
