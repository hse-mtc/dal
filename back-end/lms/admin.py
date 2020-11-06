from django.contrib import admin

from .models import (
    # Reference models
    AbsenceType,
    EncouragementType,
    Milfaculty,
    PunishmentType,
    Rank,
    Status,
    Program,
    TeacherPost,

    # Other models
    Milgroup,
    Student,
    Teacher,
    Absence,
    Encouragement,
    Punishment)

# Registering reference models
admin.site.register(AbsenceType)
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
