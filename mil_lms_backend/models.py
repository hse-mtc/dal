# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Absence(models.Model):
    date = models.DateField(primary_key=True)
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    type = models.CharField(max_length=20)
    reason = models.CharField(max_length=100, blank=True, null=True)
    status = models.DecimalField(max_digits=1, decimal_places=0)
    comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'absence'
        unique_together = (('date', 'studentid'),)


class Abstype(models.Model):
    abstype = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'abstype'


class Activity(models.Model):
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    year = models.DecimalField(max_digits=4, decimal_places=0)
    acttype = models.ForeignKey('Acttype', models.DO_NOTHING, db_column='acttype')
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'activity'


class Acttype(models.Model):
    acttype = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'acttype'


class Controlform(models.Model):
    controlform = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'controlform'


class Course(models.Model):
    course = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'course'


class Encouragement(models.Model):
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    reason = models.CharField(max_length=200)
    enctype = models.ForeignKey('Enctype', models.DO_NOTHING, db_column='enctype')
    date = models.DateField()
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherid')

    class Meta:
        db_table = 'encouragement'


class Enctype(models.Model):
    enctype = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'enctype'


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    topic = models.DecimalField(max_digits=2, decimal_places=0)
    lessonnum = models.DecimalField(max_digits=2, decimal_places=0)
    lestype = models.ForeignKey('Lestype', models.DO_NOTHING, db_column='lestype')
    date = models.DateField()
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherid')
    time = models.DecimalField(max_digits=1, decimal_places=0)
    place = models.ForeignKey('Place', models.DO_NOTHING, db_column='place')

    class Meta:
        db_table = 'lesson'


class LessonMilgroup(models.Model):
    lessonid = models.OneToOneField(Lesson, models.DO_NOTHING, db_column='lessonid', primary_key=True)
    milgroup = models.ForeignKey('Milgroup', models.DO_NOTHING, db_column='milgroup')

    class Meta:
        db_table = 'lesson-milgroup'
        unique_together = (('lessonid', 'milgroup'),)


class Lestype(models.Model):
    lestype = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'lestype'


class Mark(models.Model):
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    mark = models.DecimalField(max_digits=1, decimal_places=0)
    controlform = models.ForeignKey(Controlform, models.DO_NOTHING, db_column='controlform')
    lessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='lessonid', blank=True, null=True)

    class Meta:
        db_table = 'mark'


class Milfaculty(models.Model):
    milfaculty = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return str(self.milfaculty)

    class Meta:
        db_table = 'milfaculty'


class Milgroup(models.Model):
    milgroup = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty')

    class Meta:
        db_table = 'milgroup'


class Place(models.Model):
    place = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'place'


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=8)
    program = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'program'


class Punishment(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0)
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    reason = models.CharField(max_length=200)
    puntype = models.ForeignKey('Puntype', models.DO_NOTHING, db_column='puntype')
    date = models.DateField()
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherid')
    removedate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'punishment'


class Puntype(models.Model):
    puntype = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'puntype'


class Rank(models.Model):
    rank = models.CharField(primary_key=True, max_length=30)

    class Meta:
        db_table = 'rank'


class Skill(models.Model):
    skill = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'skill'


class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=20)

    class Meta:
        db_table = 'status'


class Student(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty')
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING, db_column='milgroup')
    birthdate = models.DateField()
    program = models.ForeignKey(Program, models.DO_NOTHING, db_column='program')
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='status')
    photo = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'student'


class StudentSkill(models.Model):
    skill = models.ForeignKey(Skill, models.DO_NOTHING, db_column='skill')
    studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='studentid', primary_key=True)

    class Meta:
        db_table = 'student-skill'
        unique_together = (('studentid', 'skill'),)


class StudentStudentpost(models.Model):
    studentpost = models.ForeignKey('Studentpost', models.DO_NOTHING, db_column='studentpost')
    studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='studentid', primary_key=True)

    class Meta:
        db_table = 'student-studentpost'
        unique_together = (('studentid', 'studentpost'),)


class Studentpost(models.Model):
    studentpost = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'studentpost'


class Teacher(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty')
    rank = models.ForeignKey(Rank, models.DO_NOTHING, db_column='rank')
    post = models.ForeignKey('Teacherpost', models.DO_NOTHING, db_column='post')
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING, db_column='milgroup', blank=True, null=True)

    class Meta:
        db_table = 'teacher'


class Teacherpost(models.Model):
    teacherpost = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'teacherpost'


class Users(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty', blank=True, null=True)
    access = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
