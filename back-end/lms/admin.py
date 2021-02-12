from django.contrib import admin

from lms.models.common import Milgroup, Milfaculty
from lms.models.student import Status, Program, Student, MilSpecialty
from lms.models.teacher import Rank, TeacherPost, Teacher
from lms.models.absence import AbsenceType, AbsenceStatus, Absence
from lms.models.encouragement import EncouragementType, Encouragement
from lms.models.punishment import PunishmentType, Punishment
from lms.models.achievement import AchievementType, Achievement
from lms.models.lesson import Room, LessonType, Lesson

# Registering reference models
admin.site.register(AbsenceType)
admin.site.register(AbsenceStatus)
admin.site.register(EncouragementType)
admin.site.register(Milfaculty)
admin.site.register(PunishmentType)
admin.site.register(Rank)
admin.site.register(Status)
admin.site.register(Program)
admin.site.register(TeacherPost)
admin.site.register(AchievementType)
admin.site.register(Room)
admin.site.register(LessonType)

# Registering other models
admin.site.register(Milgroup)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Absence)
admin.site.register(Encouragement)
admin.site.register(Punishment)
admin.site.register(Achievement)
admin.site.register(Lesson)
admin.site.register(MilSpecialty)
