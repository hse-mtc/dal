from django.db import models
import datetime


class AbsenceType(models.Model):
    absenceType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.absenceType)

    class Meta:
        db_table = 'absenceType'
        verbose_name = 'Absence Type'
        verbose_name_plural = 'Absence Types'


class ActivityType(models.Model):
    activityType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.activityType)

    class Meta:
        db_table = 'activityType'
        verbose_name = 'Activity Type'
        verbose_name_plural = 'Activity Types'


class ControlForm(models.Model):
    controlForm = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.controlForm)

    class Meta:
        db_table = 'controlForm'
        verbose_name = 'Form of Control'
        verbose_name_plural = 'Forms of Control'


class Course(models.Model):
    course = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.course)

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class EncouragementType(models.Model):
    encouragementType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.encouragementType)

    class Meta:
        db_table = 'encouragementType'
        verbose_name = 'Encouragement Type'
        verbose_name_plural = 'Encouragement Types'


class LessonType(models.Model):
    lessonType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.lessonType)

    class Meta:
        db_table = 'lessonType'
        verbose_name = 'Lesson Type'
        verbose_name_plural = 'Lesson Types'


class Milfaculty(models.Model):
    milfaculty = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return str(self.milfaculty)

    class Meta:
        db_table = 'milfaculty'
        verbose_name = 'Military Faculty'
        verbose_name_plural = 'Military Faculties'


class Place(models.Model):
    place = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.place)

    class Meta:
        db_table = 'place'
        verbose_name = 'Place in Military Educational Centre'
        verbose_name_plural = 'Places in Military Educational Centre'


class PunishmentType(models.Model):
    punishmentType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.punishmentType)

    class Meta:
        db_table = 'punishmentType'
        verbose_name = 'Punishment Type'
        verbose_name_plural = 'Punishment Types'


class Rank(models.Model):
    rank = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return str(self.rank)

    class Meta:
        db_table = 'rank'
        verbose_name = 'Military Rank'
        verbose_name_plural = 'Military Ranks'


class Skill(models.Model):
    skill = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.skill)

    class Meta:
        db_table = 'skill'
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return str(self.status)

    class Meta:
        db_table = 'status'
        verbose_name = 'Student Status'
        verbose_name_plural = 'Student Statuses'


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=8)
    program = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'({str(self.code)}) {str(self.program)}'

    class Meta:
        db_table = 'program'
        verbose_name = 'Educational Program'
        verbose_name_plural = 'Educational Programs'


class StudentPost(models.Model):
    studentPost = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.studentPost)

    class Meta:
        db_table = 'studentPost'
        verbose_name = 'Student Post'
        verbose_name_plural = 'Student Posts'


class TeacherPost(models.Model):
    teacherPost = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.teacherPost)

    class Meta:
        db_table = 'teacherPost'
        verbose_name = 'Teacher Post'
        verbose_name_plural = 'Teacher Posts'


class Milgroup(models.Model):
    milgroup = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty')

    def __str__(self):
        return f'{str(self.milgroup)}, {str(self.milfaculty)}'

    class Meta:
        db_table = 'milgroup'
        verbose_name = 'Military Group'
        verbose_name_plural = 'Military Groups'


class Student(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING, db_column='milgroup')
    birthdate = models.DateField()
    program = models.ForeignKey(Program, models.DO_NOTHING, db_column='program')
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='status')
    photo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} {str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Teacher(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING, db_column='milfaculty')
    rank = models.ForeignKey(Rank, models.DO_NOTHING, db_column='rank')
    post = models.ForeignKey(TeacherPost, models.DO_NOTHING, db_column='post')
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING, db_column='milgroup', blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} {str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class Absence(models.Model):
    date = models.DateField(default=datetime.date.today)
    studentid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentid')
    type = models.CharField(max_length=20)
    reason = models.CharField(max_length=100, blank=True, null=True)
    status = models.DecimalField(max_digits=1, decimal_places=0)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Date = {str(self.date)}\n' \
               f'StudentID = {str(self.studentid)}, Type={str(self.type)}\n'

    class Meta:
        db_table = 'absence'
        unique_together = (('date', 'studentid'),)
        verbose_name = 'Absence Journal'
        verbose_name_plural = 'Absence Journal'


class Activity(models.Model):
    studentid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentid')
    year = models.DecimalField(max_digits=4, decimal_places=0)
    type = models.ForeignKey(ActivityType, models.DO_NOTHING, db_column='type')
    comment = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.studentid)}\n' \
               f'Year = {str(self.year)}\n' \
               f'Type = {str(self.type)}\n'

    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity Journal'
        verbose_name_plural = 'Activity Journal'


class Encouragement(models.Model):
    studentid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentid')
    reason = models.CharField(max_length=200)
    type = models.ForeignKey(EncouragementType, models.DO_NOTHING, db_column='type')
    date = models.DateField(default=datetime.date.today)
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherid')

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.studentid)}, TeacherID = {str(self.teacherid)}\n' \
               f'Type = {str(self.type)}\n' \
               f'Date = {str(self.date)}'

    class Meta:
        db_table = 'encouragement'
        verbose_name = 'Encouragement Journal'
        verbose_name_plural = 'Encouragement Journal'


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    topic = models.DecimalField(max_digits=2, decimal_places=0)
    lessonnum = models.DecimalField(max_digits=2, decimal_places=0)
    type = models.ForeignKey(LessonType, models.DO_NOTHING, db_column='type')
    date = models.DateField(default=datetime.date.today)
    teacherid = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacherid')
    time = models.DecimalField(max_digits=1, decimal_places=0)
    place = models.ForeignKey(Place, models.DO_NOTHING, db_column='place')

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Course = {str(self.course)}, Date = {str(self.date)}' \
               f'TeacherID = {str(self.teacherid)}\n'

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Lessons Journal'
        verbose_name_plural = 'Lessons Journal'


class Mark(models.Model):
    studentid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentid')
    mark = models.DecimalField(max_digits=1, decimal_places=0)
    controlform = models.ForeignKey(ControlForm, models.DO_NOTHING, db_column='controlForm')
    lessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='lessonid', blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.studentid)}, LessonID = {str(self.lessonid)}\n' \
               f'Mark = {str(self.mark)}, Controlform = {str(self.controlform)}\n'

    class Meta:
        db_table = 'mark'
        verbose_name = 'Marks Journal'
        verbose_name_plural = 'Marks Journal'


class Punishment(models.Model):
    studentid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentid')
    reason = models.CharField(max_length=200)
    type = models.ForeignKey(PunishmentType, models.DO_NOTHING, db_column='type')
    date = models.DateField(default=datetime.date.today)
    teacherid = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacherid')
    removedate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.studentid)}, TeacherID = {str(self.teacherid)}\n' \
               f'Type = {str(self.type)}\n' \
               f'Date = {str(self.date)}, Remove Date = {str(self.removedate)}'

    class Meta:
        db_table = 'punishment'
        verbose_name = 'Punishment Journal'
        verbose_name_plural = 'Punishment Journal'


class LessonMilgroup(models.Model):
    lessonid = models.OneToOneField(Lesson, models.DO_NOTHING, db_column='lessonid')
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING, db_column='milgroup')

    def __str__(self):
        return f'LessonId = {str(self.lessonid)} ~ Milgroup = {str(self.milgroup)}'

    class Meta:
        db_table = 'lesson-milgroup'
        unique_together = (('lessonid', 'milgroup'),)
        verbose_name = 'Lesson-Milgroup table'
        verbose_name_plural = 'Lesson-Milgroup table'


class StudentStudentpost(models.Model):
    studentPost = models.ForeignKey(StudentPost, models.DO_NOTHING, db_column='studentPost')
    studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='studentid')

    def __str__(self):
        return f'StudentID = {str(self.studentid)} ~ StudentPost = {str(self.studentPost)}'

    class Meta:
        db_table = 'student-studentpost'
        unique_together = (('studentid', 'studentPost'),)
        verbose_name = 'Student-Studentpost table'
        verbose_name_plural = 'Student-Studentpost table'


class StudentSkill(models.Model):
    skill = models.ForeignKey(Skill, models.DO_NOTHING, db_column='skill')
    studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='studentid')

    def __str__(self):
        return f'StudentID = {str(self.studentid)} ~ Skill = {str(self.skill)}'

    class Meta:
        db_table = 'student-skill'
        unique_together = (('studentid', 'skill'),)
        verbose_name = 'Student-Skill table'
        verbose_name_plural = 'Student-Skill table'


