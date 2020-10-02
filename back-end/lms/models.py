import datetime

from django.db import models


class AbsenceType(models.Model):
    absence_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.absence_type)

    class Meta:
        db_table = 'absence_type'
        verbose_name = 'Absence Type'
        verbose_name_plural = 'Absence Types'


class AbsenceStatus(models.Model):
    absence_status = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.absence_status)

    class Meta:
        db_table = 'absence_status'
        verbose_name = 'Absence Status'
        verbose_name_plural = 'Absence Statuses'


class ActivityType(models.Model):
    activity_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.activity_type)

    class Meta:
        db_table = 'activity_type'
        verbose_name = 'Activity Type'
        verbose_name_plural = 'Activity Types'


class ControlForm(models.Model):
    control_form = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.control_form)

    class Meta:
        db_table = 'control_form'
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
    encouragement_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.encouragement_type)

    class Meta:
        db_table = 'encouragement_type'
        verbose_name = 'Encouragement Type'
        verbose_name_plural = 'Encouragement Types'


class LessonType(models.Model):
    lesson_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.lesson_type)

    class Meta:
        db_table = 'lesson_type'
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
    punishment_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.punishment_type)

    class Meta:
        db_table = 'punishment_type'
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
    student_post = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.student_post)

    class Meta:
        db_table = 'student_post'
        verbose_name = 'Student Post'
        verbose_name_plural = 'Student Posts'


class TeacherPost(models.Model):
    teacher_post = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.teacher_post)

    class Meta:
        db_table = 'teacher_post'
        verbose_name = 'Teacher Post'
        verbose_name_plural = 'Teacher Posts'


class Milgroup(models.Model):
    milgroup = models.DecimalField(primary_key=True,
                                   max_digits=4,
                                   decimal_places=0)
    milfaculty = models.ForeignKey(Milfaculty,
                                   models.DO_NOTHING,
                                   db_column='milfaculty')
    weekday = models.DecimalField(max_digits=1, decimal_places=0)

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
    milgroup = models.ForeignKey(Milgroup,
                                 models.DO_NOTHING,
                                 db_column='milgroup')
    birthdate = models.DateField()
    program = models.ForeignKey(Program, models.DO_NOTHING, db_column='program')
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='status')
    photo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Teacher(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    milfaculty = models.ForeignKey(Milfaculty,
                                   models.DO_NOTHING,
                                   db_column='milfaculty')
    rank = models.ForeignKey(Rank, models.DO_NOTHING, db_column='rank')
    teacher_post = models.ForeignKey(TeacherPost,
                                     models.DO_NOTHING,
                                     db_column='teacher_post')
    milgroup = models.ForeignKey(Milgroup,
                                 models.DO_NOTHING,
                                 db_column='milgroup',
                                 blank=True,
                                 null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class Absence(models.Model):
    date = models.DateField(default=datetime.date.today)
    student = models.ForeignKey(Student, models.CASCADE, db_column='student')
    absence_type = models.ForeignKey(AbsenceType,
                                     models.DO_NOTHING,
                                     db_column='absence_type')
    absence_status = models.ForeignKey(AbsenceStatus,
                                       models.DO_NOTHING,
                                       db_column='absence_status')
    reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Date = {str(self.date)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'Absence type={str(self.absence_type)}\n'

    class Meta:
        db_table = 'absence'
        unique_together = (('date', 'student'),)
        verbose_name = 'Absence Journal'
        verbose_name_plural = 'Absence Journal'


class Activity(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, db_column='student')
    year = models.DecimalField(max_digits=4, decimal_places=0)
    activity_type = models.ForeignKey(ActivityType,
                                      models.DO_NOTHING,
                                      db_column='activity_type')
    comment = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}\n' \
               f'Year = {str(self.year)}\n' \
               f'Type = {str(self.activity_type)}\n'

    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity Journal'
        verbose_name_plural = 'Activity Journal'


class Encouragement(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, db_column='student')
    reason = models.CharField(max_length=200)
    encouragement_type = models.ForeignKey(EncouragementType,
                                           models.DO_NOTHING,
                                           db_column='encouragement_type')
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey('Teacher',
                                models.DO_NOTHING,
                                db_column='teacher')

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'TeacherID = {str(self.teacher)}\n' \
               f'Type = {str(self.encouragement_type)}\n' \
               f'Date = {str(self.date)}'

    class Meta:
        db_table = 'encouragement'
        verbose_name = 'Encouragement Journal'
        verbose_name_plural = 'Encouragement Journal'


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    topic = models.DecimalField(max_digits=2, decimal_places=0)
    lesson_num = models.DecimalField(max_digits=2, decimal_places=0)
    lesson_type = models.ForeignKey(LessonType,
                                    models.DO_NOTHING,
                                    db_column='type')
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher')
    time = models.DecimalField(max_digits=1, decimal_places=0)
    place = models.ForeignKey(Place, models.DO_NOTHING, db_column='place')

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Course = {str(self.course)}, Date = {str(self.date)}' \
               f'TeacherID = {str(self.teacher)}\n'

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Lessons Journal'
        verbose_name_plural = 'Lessons Journal'


class Mark(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, db_column='student')
    mark = models.DecimalField(max_digits=1, decimal_places=0)
    control_form = models.ForeignKey(ControlForm,
                                     models.DO_NOTHING,
                                     db_column='control_form')
    lesson = models.ForeignKey(Lesson,
                               models.DO_NOTHING,
                               db_column='lesson',
                               blank=True,
                               null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, '\
               f'LessonID = {str(self.lesson)}\n' \
               f'Mark = {str(self.mark)}, '\
               f'Controlform = {str(self.control_form)}\n'

    class Meta:
        db_table = 'mark'
        verbose_name = 'Marks Journal'
        verbose_name_plural = 'Marks Journal'


class Punishment(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, db_column='student')
    reason = models.CharField(max_length=200)
    punishment_type = models.ForeignKey(PunishmentType,
                                        models.DO_NOTHING,
                                        db_column='punishment_type')
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher')
    remove_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'TeacherID = {str(self.teacher)}\n' \
               f'Type = {str(self.punishment_type)}\n' \
               f'Date = {str(self.date)}, ' \
               f'Remove Date = {str(self.remove_date)}'

    class Meta:
        db_table = 'punishment'
        verbose_name = 'Punishment Journal'
        verbose_name_plural = 'Punishment Journal'


class LessonMilgroup(models.Model):
    lesson = models.OneToOneField(Lesson, models.DO_NOTHING, db_column='lesson')
    milgroup = models.ForeignKey(Milgroup,
                                 models.DO_NOTHING,
                                 db_column='milgroup')

    def __str__(self):
        return f'LessonId = {str(self.lesson)} ~ ' \
               f'Milgroup = {str(self.milgroup)}'

    class Meta:
        db_table = 'lesson-milgroup'
        unique_together = (('lesson', 'milgroup'),)
        verbose_name = 'Lesson-Milgroup table'
        verbose_name_plural = 'Lesson-Milgroup table'


class StudentStudentpost(models.Model):
    student_post = models.ForeignKey(StudentPost,
                                     models.DO_NOTHING,
                                     db_column='student_post')
    student = models.OneToOneField(Student,
                                   models.DO_NOTHING,
                                   db_column='student')

    def __str__(self):
        return f'StudentID = {str(self.student)} ~ ' \
               f'StudentPost = {str(self.student_post)}'

    class Meta:
        db_table = 'student-studentpost'
        unique_together = (('student', 'student_post'),)
        verbose_name = 'Student-Studentpost table'
        verbose_name_plural = 'Student-Studentpost table'


class StudentSkill(models.Model):
    skill = models.ForeignKey(Skill, models.DO_NOTHING, db_column='skill')
    student = models.OneToOneField(Student,
                                   models.DO_NOTHING,
                                   db_column='student')

    def __str__(self):
        return f'StudentID = {str(self.student)} ~ Skill = {str(self.skill)}'

    class Meta:
        db_table = 'student-skill'
        unique_together = (('student', 'skill'),)
        verbose_name = 'Student-Skill table'
        verbose_name_plural = 'Student-Skill table'
