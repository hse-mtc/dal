from django.contrib import admin

from lms.models.common import Milgroup, Milfaculty
from lms.models.student import Status, Program, Student
from lms.models.teacher import Rank, TeacherPost, Teacher
from lms.models.absence import AbsenceType, AbsenceStatus, Absence
from lms.models.encouragement import EncouragementType, Encouragement
from lms.models.punishment import PunishmentType, Punishment

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

# Registering other models
admin.site.register(Milgroup)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Absence)
admin.site.register(Encouragement)
admin.site.register(Punishment)
