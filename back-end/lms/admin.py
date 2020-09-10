from django.contrib import admin

from .models import (
    # Reference models
    AbsenceType,
    ActivityType,
    ControlForm,
    Course,
    EncouragementType,
    LessonType,
    Milfaculty,
    Place,
    PunishmentType,
    Rank,
    Skill,
    Status,
    Program,
    StudentPost,
    TeacherPost,

    # Other models
    Milgroup,
    Student,
    Teacher,
    Absence,
    Activity,
    Encouragement,
    Lesson,
    Mark,
    Punishment,

    # Models used for ManyToMany Relationships
    LessonMilgroup,
    StudentStudentpost,
    StudentSkill)

# Registering reference models
admin.site.register(AbsenceType)
admin.site.register(ActivityType)
admin.site.register(ControlForm)
admin.site.register(Course)
admin.site.register(EncouragementType)
admin.site.register(LessonType)
admin.site.register(Milfaculty)
admin.site.register(Place)
admin.site.register(PunishmentType)
admin.site.register(Rank)
admin.site.register(Skill)
admin.site.register(Status)
admin.site.register(Program)
admin.site.register(StudentPost)
admin.site.register(TeacherPost)

# Registering other models
admin.site.register(Milgroup)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Absence)
admin.site.register(Activity)
admin.site.register(Encouragement)
admin.site.register(Lesson)
admin.site.register(Mark)
admin.site.register(Punishment)

# Registering ManyToMany Relationships models
admin.site.register(LessonMilgroup)
admin.site.register(StudentStudentpost)
admin.site.register(StudentSkill)
